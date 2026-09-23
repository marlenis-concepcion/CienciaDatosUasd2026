import numpy as np
import pytest

tf = pytest.importorskip("tensorflow")
from inf8239_u03_gen.models import build_autoencoder, build_encoder_decoder


def test_autoencoder_output_contract():
    model = build_autoencoder(tf)
    result = model(np.zeros((2, 28, 28, 1), dtype="float32")).numpy()
    assert result.shape == (2, 28, 28, 1)


def test_decoder_output_contract():
    _, decoder = build_encoder_decoder(tf, latent_dim=2)
    result = decoder(np.zeros((2, 2), dtype="float32")).numpy()
    assert result.shape == (2, 28, 28, 1)


def test_encoder_returns_mean_and_log_variance_with_latent_size():
    encoder, _ = build_encoder_decoder(tf, latent_dim=16)
    mean, log_variance = encoder(np.zeros((3, 28, 28, 1), dtype="float32"))
    assert mean.shape == (3, 16) and log_variance.shape == (3, 16)


def test_vae_losses_are_finite_and_kl_is_non_negative():
    from inf8239_u03_gen.models import make_vae_class

    encoder, decoder = build_encoder_decoder(tf, latent_dim=2)
    vae = make_vae_class(tf)(encoder, decoder)
    images = np.random.default_rng(0).random((4, 28, 28, 1)).astype("float32")
    reconstruction, kl = vae.losses_for(images, False)
    assert np.isfinite(float(reconstruction)) and float(kl) >= 0
