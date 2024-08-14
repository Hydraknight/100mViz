import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import matplotlib.font_manager as font_manager

# Athlete times data
athletes = {
    "JACOBS Lamont Marcell": [1.87, 2.92, 3.85, 4.74, 5.60, 6.44, 7.28, 8.13, 8.98, 9.85],
    "TEBOGO Letsile": [1.90, 2.94, 3.87, 4.75, 5.61, 6.45, 7.29, 8.13, 8.98, 9.86],
    "LYLES Noah": [1.95, 2.98, 3.90, 4.76, 5.61, 6.44, 7.26, 8.09, 8.93, 9.786],
    "SEVILLE Oblique": [1.89, 2.94, 3.87, 4.75, 5.60, 6.45, 7.29, 8.13, 9.00, 9.91],
    "SIMBINE Akani": [1.90, 2.95, 3.87, 4.75, 5.60, 6.46, 7.27, 8.11, 8.96, 9.82],
    "THOMPSON Kishane": [1.90, 2.93, 3.84, 4.72, 5.56, 6.41, 7.24, 8.07, 8.92, 9.79],
    "KERLEY Fred": [1.87, 2.92, 3.85, 4.73, 5.58, 6.41, 7.25, 8.09, 8.94, 9.81],
    "BEDNAREK Kenneth": [1.91, 2.96, 3.88, 4.75, 5.61, 6.46, 7.29, 8.14, 9.00, 9.88]
}

track_length = 100  # in meters
num_lanes = 8

# Initialize finishing times
finishing_times = {athlete: times[-1] for athlete, times in athletes.items()}

# Linearly interpolate each data point to create intervals between each recorded time


def interpolate_times(times, num_points=1):
    distances = np.linspace(0, track_length, len(times))
    interpolated_distances = np.linspace(
        0, track_length, len(times) * num_points - (num_points - 1))
    interpolated_times = np.interp(interpolated_distances, distances, times)
    return interpolated_distances, interpolated_times


# Interpolating all athlete times
interpolated_athletes = {athlete: interpolate_times(
    times)[1] for athlete, times in athletes.items()}

# Creating the plot
fig, ax = plt.subplots(figsize=(25, 10))
ax.set_xlim(0, track_length)
ax.set_ylim(-0.5, num_lanes + 0.5)
ax.set_xlabel('Distance (m)', fontsize=12, color='white')
ax.set_ylabel('Lane', fontsize=12, color='white')
plt.yticks([])
# Set black background
fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# Draw lanes with the specified color and white lines between tracks
lane_color = "#b1a4fc"
font_path_bold = "font.ttf"
legend_text_prop = font_manager.FontProperties(fname=font_path_bold, size=32)
lanes = []
for i in range(num_lanes):
    lane = ax.add_patch(patches.Rectangle((0, i - 0.5), track_length,
                                          1, linewidth=1, facecolor=lane_color))
    lanes.append(lane)
    ax.text(
        -1, i, f"{9-i}", color='white', ha='center', va='center', fontproperties=legend_text_prop
    )
    ax.axhline(y=i + 0.5, color='white', linewidth=5)
# Initialize the dots and labels
dots = []
labels = []
for i, (athlete, times) in enumerate(athletes.items()):
    dot, = ax.plot(0, i, 'o', color="black", markersize=10, label=athlete)
    label = ax.text(
        0, i, athlete, color="black",  ha='right', va='center', fontproperties=legend_text_prop)
    dots.append(dot)
    labels.append(label)

# Track athletes who have finished and their finishing order
finished_athletes = []

# Track which distance markers (20m, 40m, 60m, 80m) have been crossed
distance_markers = [20, 40, 60, 80]
crossed_markers = []


def update(frame):
    current_time = frame / 30
    for i, (athlete, times) in enumerate(interpolated_athletes.items()):
        current_position = np.interp(
            current_time, times, np.linspace(0, track_length, len(times)))
        dots[i].set_xdata(current_position)
        labels[i].set_x(max(0, current_position - 1))

        # Check if athlete has finished and assign finishing order
        if athlete not in finished_athletes and current_position >= track_length:
            for j, ath in enumerate(finishing_times):
                if finishing_times[ath] == min(finishing_times.values()):
                    finished_athletes.append(athlete)
                    finishing_times[ath] = 999
                    break
            if len(finished_athletes) == 1:
                lanes[j].set_facecolor('gold')
            elif len(finished_athletes) == 2:
                lanes[j].set_facecolor('silver')
            elif len(finished_athletes) == 3:
                lanes[j].set_facecolor('#CD7F32') #bronze

        # Check if a 20m marker has been crossed by the first athlete
        for marker in distance_markers:
            if marker not in crossed_markers and current_position >= marker:
                for k, (ath, ath_times) in enumerate(interpolated_athletes.items()):
                    ath_position = np.interp(
                        current_time, ath_times, np.linspace(0, track_length, len(ath_times)))
                    ax.plot([ath_position, ath_position], [
                            k - 0.5, k + 0.5], color='black', linestyle='--', linewidth=2)
                crossed_markers.append(marker)

    return dots + labels + lanes


max_time = max([times[-1] for times in athletes.values()])
frames = int(max_time * 30)

# Create animation
ani = animation.FuncAnimation(
    fig, update, frames=frames+60, interval=33, blit=True)  # 33ms per frame for 30 fps

# Adding title
plt.title('Men\'s 100m Final Visualization',
          fontproperties=legend_text_prop, color='white')

# Customize ticks
ax.tick_params(axis='both', colors='white')
plt.ylabel("")
# Add finish line
ax.axvline(x=100, color='white', linestyle='--', linewidth=3)
ax.text(100, num_lanes + 0.6, 'Finish', color='white',
        ha='center', va='bottom', fontproperties=legend_text_prop)

# Save the GIF
ani.save('100m_mens_final_interpolated.gif', writer='pillow',
         fps=30, savefig_kwargs={'facecolor': 'black'})
plt.show()
