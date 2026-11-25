import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider


AMPLITUDE = 1.0
INITIAL_FREQUENCY = 5.0
INITIAL_SAMPLING_FREQUENCY = 20.0
DURATION = 1.0


def generate_signal(signal_frequency):
    dense_time = np.linspace(0.0, DURATION, 5000)
    original_signal = AMPLITUDE * np.sin(2.0 * np.pi * signal_frequency * dense_time)
    return dense_time, original_signal


def reconstruct_signal(dense_time, sample_times, sample_values, sampling_frequency):
    reconstructed = np.zeros_like(dense_time)
    sampling_period = 1.0 / sampling_frequency

    for sample_time, sample_value in zip(sample_times, sample_values):
        reconstructed += sample_value * np.sinc(
            (dense_time - sample_time) / sampling_period
        )

    return reconstructed


def main():
    figure, axes = plt.subplots(3, 1, figsize=(10, 7))
    figure.suptitle("Signal Sampling and Reconstruction Simulator")
    plt.subplots_adjust(left=0.10, right=0.98, bottom=0.25, hspace=0.55)

    dense_time, original_signal = generate_signal(INITIAL_FREQUENCY)
    initial_sampling_period = 1.0 / INITIAL_SAMPLING_FREQUENCY
    sample_times = np.arange(
        0.0,
        DURATION + initial_sampling_period / 2.0,
        initial_sampling_period,
    )
    sample_values = AMPLITUDE * np.sin(
        2.0 * np.pi * INITIAL_FREQUENCY * sample_times
    )
    reconstructed = reconstruct_signal(
        dense_time,
        sample_times,
        sample_values,
        INITIAL_SAMPLING_FREQUENCY,
    )

    (original_line,) = axes[0].plot(dense_time, original_signal, color="blue")
    axes[0].set_title("Original Sinusoidal Signal")
    axes[0].set_ylabel("Amplitude")
    axes[0].set_ylim(-1.2, 1.2)
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(dense_time, original_signal, color="lightgray", linewidth=1)
    (sample_line,) = axes[1].plot(
        sample_times,
        sample_values,
        "o",
        color="red",
        markersize=4,
    )
    axes[1].set_title("Sampled Signal")
    axes[1].set_ylabel("Amplitude")
    axes[1].set_ylim(-1.2, 1.2)
    axes[1].grid(True, alpha=0.3)

    (reconstructed_line,) = axes[2].plot(
        dense_time,
        reconstructed,
        color="green",
    )
    axes[2].plot(dense_time, original_signal, "--", color="black", alpha=0.5)
    axes[2].set_title("Sinc Reconstruction")
    axes[2].set_xlabel("Time (seconds)")
    axes[2].set_ylabel("Amplitude")
    axes[2].set_ylim(-1.2, 1.2)
    axes[2].grid(True, alpha=0.3)

    for axis in axes:
        axis.set_xlim(0.0, DURATION)

    status_text = figure.text(
        0.10,
        0.205,
        "",
        fontsize=10,
        color="green",
        ha="left",
    )

    frequency_slider_axis = figure.add_axes([0.15, 0.135, 0.70, 0.03])
    sampling_slider_axis = figure.add_axes([0.15, 0.085, 0.70, 0.03])
    reset_axis = figure.add_axes([0.85, 0.020, 0.10, 0.035])

    frequency_slider = Slider(
        frequency_slider_axis,
        "Signal frequency (Hz)",
        1.0,
        20.0,
        valinit=INITIAL_FREQUENCY,
        valstep=1.0,
    )
    sampling_slider = Slider(
        sampling_slider_axis,
        "Sampling frequency (Hz)",
        5.0,
        50.0,
        valinit=INITIAL_SAMPLING_FREQUENCY,
        valstep=1.0,
    )
    reset_button = Button(reset_axis, "Reset")

    def update(_):
        signal_frequency = frequency_slider.val
        sampling_frequency = sampling_slider.val

        dense_time, original_signal = generate_signal(signal_frequency)
        sampling_period = 1.0 / sampling_frequency
        sample_times = np.arange(
            0.0,
            DURATION + sampling_period / 2.0,
            sampling_period,
        )
        sample_values = AMPLITUDE * np.sin(
            2.0 * np.pi * signal_frequency * sample_times
        )
        reconstructed = reconstruct_signal(
            dense_time,
            sample_times,
            sample_values,
            sampling_frequency,
        )

        original_line.set_xdata(dense_time)
        original_line.set_ydata(original_signal)

        axes[1].lines[0].set_xdata(dense_time)
        axes[1].lines[0].set_ydata(original_signal)
        sample_line.set_xdata(sample_times)
        sample_line.set_ydata(sample_values)

        reconstructed_line.set_xdata(dense_time)
        reconstructed_line.set_ydata(reconstructed)
        axes[2].lines[1].set_xdata(dense_time)
        axes[2].lines[1].set_ydata(original_signal)

        nyquist_rate = 2.0 * signal_frequency
        if sampling_frequency >= nyquist_rate:
            status_text.set_text(
                f"Nyquist criterion satisfied: fs = {sampling_frequency:.0f} Hz "
                f">= 2fm = {nyquist_rate:.0f} Hz"
            )
            status_text.set_color("green")
        else:
            status_text.set_text(
                f"Undersampling warning: fs = {sampling_frequency:.0f} Hz "
                f"< 2fm = {nyquist_rate:.0f} Hz"
            )
            status_text.set_color("red")

        figure.canvas.draw_idle()

    def reset(_):
        frequency_slider.reset()
        sampling_slider.reset()

    frequency_slider.on_changed(update)
    sampling_slider.on_changed(update)
    reset_button.on_clicked(reset)
    update(None)

    plt.show()


if __name__ == "__main__":
    main()
