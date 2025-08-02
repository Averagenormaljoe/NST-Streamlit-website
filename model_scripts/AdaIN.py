from keras.saving import register_keras_serializable
import keras
import tensorflow as tf

@register_keras_serializable()
class NeuralStyleTransfer(tf.keras.Model):
    def __init__(self, encoder, decoder, loss_net, style_weight, **kwargs):
        super(NeuralStyleTransfer, self).__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder
        self.loss_net = loss_net
        self.style_weight = style_weight
        self.is_log = False
        self.include_custom_metrics = False
        self.hardwareLogger = TFHardwareLogger()
    def train_start(self):
        if self.is_log:
            self.hardwareLogger.train_start()
    def train_end(self):
        if self.is_log:
            self.hardwareLogger.train_end()

    def compile(self, optimizer, loss_fn):
        super().compile()
        self.optimizer = optimizer
        self.loss_fn = loss_fn
        self.style_loss_tracker = keras.metrics.Mean(name="style_loss")
        self.content_loss_tracker = keras.metrics.Mean(name="content_loss")
        self.total_loss_tracker = keras.metrics.Mean(name="total_loss")
        self.psnr_tracker = keras.metrics.Mean(name="psnr")
        self.ssim_tracker = keras.metrics.Mean(name="ssim")
        self.lpips_tracker = keras.metrics.Mean(name="lpips")
        self.tv_loss_tracker = keras.metrics.Mean(name="tv_loss")
    def reconstruct_image(self, style, content):
        # Encode the style and content image.
        style_encoded = self.encoder(style)
        content_encoded = self.encoder(content)
        # Compute the AdaIN target feature maps.
        t = ada_in(style=style_encoded, content=content_encoded)
        # Generate the neural style transferred image.
        reconstructed_image = self.decoder(t)
        return reconstructed_image,t

    def compute_custom_loss(self, content,reconstructed_image):
        if self.include_custom_metrics:
            psnr = psnr_loss(content, reconstructed_image, val_range=1.0)
            ssim = ssim_loss(content, reconstructed_image, val_range=1.0)
            lpips = get_lpips_loss(content, reconstructed_image, loss_net="vgg19")
            return psnr, ssim, lpips
        return 0,0,0

    def get_results(self):
        return {
            "style_loss": self.style_loss_tracker.result(),
            "content_loss": self.content_loss_tracker.result(),
            "total_loss": self.total_loss_tracker.result(),
            "tv_loss": self.tv_loss_tracker.result(),
            "psnr": self.psnr_tracker.result(),
            "ssim": self.ssim_tracker.result(),
            "lpips" : self.lpips_tracker.result(),

        }


    def all_update_state(self, style_loss : float, content_loss : float, total_loss : float, tv_loss : float, psnr, ssim : float,lpips_loss : float):
        # Update the trackers.
        self.style_loss_tracker.update_state(style_loss)
        self.content_loss_tracker.update_state(content_loss)
        self.total_loss_tracker.update_state(total_loss)
        # new metrics
        self.tv_loss_tracker.update_state(tv_loss)
        self.psnr_tracker.update_state(psnr)
        self.ssim_tracker.update_state(ssim)
        self.lpips_tracker.update_state(lpips_loss)

    def apply_optimizer(self, gradients,trainable_vars):
        self.optimizer.apply_gradients(zip(gradients, trainable_vars))
    def compute_gradients(self,total_loss, tape):
        trainable_vars = self.decoder.trainable_variables
        gradients = tape.gradient(total_loss, trainable_vars)
        self.apply_optimizer(gradients, trainable_vars)
        return gradients
    def calculate_temporal_loss(self, content_image, reconstructed_image):
        temporal_loss = 0
        return temporal_loss
    def compute_loop_loss_style(self, mean_inp, mean_out, std_inp, std_out):
        loss_style = self.loss_fn(mean_inp, mean_out) + self.loss_fn(std_inp, std_out)
        return loss_style
    def compute_total_variation(self,reconstructed_image):
        total_variation_loss = tf.reduce_mean(tf.image.total_variation(reconstructed_image))
        return total_variation_loss
    def compute_total_loss(self, loss_content : float,loss_style : float, tv_loss : float) -> float:
        total_loss = loss_content + loss_style + 1e-6 * tv_loss
        return total_loss
    def compute_loss_style(self, style_vgg_features, recons_vgg_features):
        # Initialize the style loss.
        loss_style = 0.0
        for inp, out in zip(style_vgg_features, recons_vgg_features):
            mean_inp, std_inp = get_mean_std(inp)
            mean_out, std_out = get_mean_std(out)
            loss_style += self.compute_loop_loss_style(mean_inp,mean_out,std_inp,std_out)
        return loss_style
    def compute_losses(self, style, t, reconstructed_image):
        # Initialize the content loss.
        loss_content = 0.0
        # Compute the losses.
        recons_vgg_features = self.loss_net(reconstructed_image)
        style_vgg_features = self.loss_net(style)
        loss_content = self.loss_fn(t, recons_vgg_features[-1])
        loss_style = self.compute_loss_style(style_vgg_features, recons_vgg_features)
        loss_style = self.style_weight * loss_style
        return loss_content,loss_style

    def generate_image_and_losses(self,style,content):
        # Reconstruct the image
        reconstructed_image,t = self.reconstruct_image(style, content)
        # Compute the losses.
        loss_content, loss_style = self.compute_losses(style, t, reconstructed_image)
        return reconstructed_image, loss_content, loss_style,t

    def process_inputs(self,inputs):
        # Unpack the inputs.
        style, content = inputs
        return style,content

    def log_hardware(self):
        if self.is_log:
            self.hardwareLogger.log_hardware()

    def train_step(self, inputs):

        self.train_start()
        style, content = inputs
        with tf.GradientTape() as tape:
            # Reconstruct the image.
            reconstructed_image,loss_content, loss_style,t = self.generate_image_and_losses(style,content)
            tv_loss = self.compute_total_variation(reconstructed_image)
            # Compute the total variation loss.
            total_loss = self.compute_total_loss(loss_content, loss_style, tv_loss)
            # Compute custom metrics.
            psnr, ssim,lpips = self.compute_custom_loss(content, reconstructed_image)

        # Compute gradients and optimize the decoder.
        gradients = self.compute_gradients(total_loss, tape)
        # Update the trackers.
        self.all_update_state(loss_style, loss_content, total_loss, tv_loss, psnr, ssim,lpips)

        # metrics

        self.log_hardware()
        self.train_end()

        return self.get_results()
    def test_step(self, inputs):
        style, content = inputs
        # Reconstruct the image.
        reconstructed_image,loss_content, loss_style,t = self.generate_image_and_losses(style,content)
        # Compute the losses.
        loss_content, loss_style = self.compute_losses(style, t, reconstructed_image)
        # Compute the total variation loss and other metrics
        tv_loss = self.compute_total_variation(reconstructed_image)
        # Compute custom metrics.
        psnr,ssim,lpips = self.compute_custom_loss(content, reconstructed_image)
        # Compute the total loss.
        total_loss = self.compute_total_loss(loss_content, loss_style, tv_loss)
        total_loss += psnr + ssim + lpips
        # Update the trackers.
        self.all_update_state(loss_style, loss_content, total_loss, tv_loss, psnr, ssim,lpips)
        return self.get_results()
    def get_resource_stats(self):
        return {
            "cpu": self.hardwareLogger.get_name_log("cpu"),
            "gpu": self.hardwareLogger.get_name_log("gpu"),
            "ram" : self.hardwareLogger.get_name_log("ram"),
            "disk": self.hardwareLogger.get_name_log("disk")
        }
    def execute_stylization(self,inputs):
        style = inputs[0]
        content = inputs[1]
        style_encoded = self.encoder(style)
        content_encoded = self.encoder(content)
        t = ada_in(style=style_encoded, content=content_encoded)
        reconstructed_image = self.decoder(t)
        return reconstructed_image
    def multi_NST(self, inputs):

        style_imgs = inputs[0]
        content = inputs[1]
        style_encoded_features = [self.encoder(s) for s in style_imgs]
        content_encoded = self.encoder(content)

        style_outputs = [ada_in(style=s, content=content_encoded) for s in style_encoded_features]
        stack = tf.stack(style_outputs)
        t = tf.reduce_mean(stack, axis=0)
        reconstructed_image = self.decoder(t)
        return reconstructed_image
    def one_step_multi_NST(self, style_images, content_encoded):
        stylized_image = content_encoded
        for s in style_images:
            style_encoded = self.encoder(s)
            features = ada_in(style=style_encoded, content=stylized_image)
            stylized_image = features

        reconstructed_image = self.decoder(stylized_image)
        return reconstructed_image
    def call(self, content_image, style_image):
        reconstructed_image = self.execute_stylization([style_image, content_image])
        return reconstructed_image



    def get_config(self):
        config = super().get_config()
        config.update({
            "encoder": keras.saving.serialize_keras_object(self.encoder),
            "decoder": keras.saving.serialize_keras_object(self.decoder),
            "loss_net": keras.saving.serialize_keras_object(self.loss_net),
            "style_weight": self.style_weight,
        })
        return config

    @classmethod
    def from_config(cls, config):

        encoder_config = config.pop("encoder")
        decoder_config = config.pop("decoder")
        loss_net_config = config.pop("loss_net")
        style_weight = config.pop("style_weight")

        encoder = keras.saving.deserialize_keras_object(encoder_config)
        decoder = keras.saving.deserialize_keras_object(decoder_config)
        loss_net = keras.saving.deserialize_keras_object(loss_net_config)

        return cls(encoder=encoder, decoder=decoder, loss_net=loss_net, style_weight=style_weight, **config)
    @property
    def metrics(self):
        return [
            self.style_loss_tracker,
            self.content_loss_tracker,
            self.total_loss_tracker,
            self.tv_loss_tracker,
            self.psnr_tracker,
            self.ssim_tracker,
            self.lpips_tracker,
        ]
