import streamlit as st
import numpy as np
from pathlib import Path
from modules.image_process import png_to_array, crop_image, compress_image_with_gaussian, compress_image
from modules.plotting_modules import (create_plotly_figure, 
                                      heatmap_plot_with_bounding_box,
                                      quiver_plot_plotly,
                                      quiver_plot_matplotlib)
from modules.phase_analysis import isoclinic_phase, isochromatic_phase

st.set_page_config(page_title="Stress Imaging Analysis", layout="wide")
st.title("Stress Imaging Analysis")

# Sidebar controls
st.sidebar.header("Analysis Settings")
phase_method = st.sidebar.selectbox(
    "Phase Calculation Method",
    ["arctan2", "arctan"],
    help="Method used to calculate phase angles"
)

# File upload section
st.header("Image Upload")
uploaded_files = st.file_uploader(
    "Upload images (I1-I10)", 
    accept_multiple_files=True,
    type=['png', 'jpg', 'jpeg']
)

if "do_cropping" not in st.session_state:
    st.session_state.do_cropping = False
if "show_cropped_images" not in st.session_state:
    st.session_state.show_cropped_images = False
if "show_full_images" not in st.session_state:
    st.session_state.show_full_images = False
if "do_compress_image" not in st.session_state:
    st.session_state.do_compress_image = False

with st.sidebar:
    colormap = st.selectbox("Colormap", ["jet", "viridis", "plasma", "inferno", "magma", "cividis", "turbo", "gray"])
    calibration_file = st.file_uploader("Upload Calibration File", 
                                        type=['png', 'jpg', 'jpeg'])
    if calibration_file:
        calib_image = png_to_array(calibration_file)
        calib_image_size = calib_image.shape
        col1, col2 = st.columns(2)
        with col1:
            crop_x0 = st.number_input("Crop X0", 
                                    value=0, 
                                    min_value=0, 
                                    max_value=calib_image_size[1], 
                                    step=1)
        with col2:
            crop_x1 = st.number_input("Crop X1", 
                                    value=calib_image_size[1], 
                                    min_value=0, 
                                    max_value=calib_image_size[1], 
                                    step=1)
        with col1:
            crop_y0 = st.number_input("Crop Y0", 
                                    value=0, 
                                    min_value=0, 
                                    max_value=calib_image_size[0], 
                                    step=1)
        with col2:
            crop_y1 = st.number_input("Crop Y1", 
                                    value=calib_image_size[0], 
                                    min_value=0, 
                                    max_value=calib_image_size[0], 
                                    step=1)
        crop_range_x = [crop_x0, crop_x1]
        crop_range_y = [crop_y0, crop_y1]
        bounding_box = [crop_x0, crop_y0, crop_x1, crop_y1]
        calib_image_cropped = crop_image(calib_image, crop_range_x, crop_range_y)
        st.session_state.do_cropping = st.checkbox("Apply Cropping to all images", value=st.session_state.do_cropping)
        st.session_state.show_full_images = st.checkbox("Show Full Images", value=st.session_state.show_full_images)
        if st.session_state.do_cropping:
            st.session_state.show_cropped_images = st.checkbox("Show Cropped Images", value=st.session_state.show_cropped_images)

if calibration_file:
    with st.expander("Calibration Image", expanded=False):
        fig = heatmap_plot_with_bounding_box(calib_image, 
                                            title="Calibration Image", 
                                            color_map="jet", 
                                            color_range=(0, 65000),
                                            fig_height=800,
                                            fig_width=800,
                                            bounding_box=bounding_box)
        st.plotly_chart(fig)

if uploaded_files:
    # Convert uploaded files to dict
    image_dict = {}
    image_dict_cropped = {}
    for idx, file in enumerate(uploaded_files):
        name = file.name.split('.')[0].upper()  # Get filename without extension
        if '_' in name:
            index_name = name.split('_')[0]
        image_array = png_to_array(file)
        image_dict[index_name] = image_array
        if st.session_state.do_cropping:
            image_array_cropped = crop_image(image_array, crop_range_x, crop_range_y)
            image_dict_cropped[index_name] = image_array_cropped
        
        # Create plotly figure
        with st.expander(f"{name} Colormap", expanded=False):
            color_range = st.slider("Color Range", 
                                            min_value=0.0, 
                                            max_value=65000.0, 
                                            value=(float(np.min(image_dict[index_name])), 
                                                   float(np.max(image_dict[index_name]))),
                                            key=f"{name}_color_range")

            fig = create_plotly_figure(image_dict[index_name], title=f"{name}", color_range=color_range, cmap=colormap)
            st.plotly_chart(fig)
            if st.session_state.show_full_images:
                fig = heatmap_plot_with_bounding_box(image_dict[index_name], 
                                                title=f"{name}", 
                                                color_map=colormap, 
                                                color_range=color_range,
                                                fig_height=800,
                                                fig_width=800,
                                                bounding_box=bounding_box)
                st.plotly_chart(fig)

            if st.session_state.do_cropping and st.session_state.show_cropped_images:
                fig_cropped = create_plotly_figure(image_dict_cropped[index_name], 
                                                title=f"{name} Cropped", 
                                                cmap=colormap, 
                                                color_range=color_range)
                st.plotly_chart(fig_cropped)

col1, col2 = st.columns(2)
with col1:
    calculate_phase = st.checkbox("Calculate Phase", value=False)
    phase_cmap = st.selectbox("Phase Colormap", 
                              ["jet", "viridis", "plasma", "inferno", "magma", "cividis", "turbo", "gray"],
                              index=0)
with col2:
    apply_isoclinic_unwrap = st.checkbox("Apply Isoclinic Unwrap", value=False)
    apply_isochromatic_unwrap = st.checkbox("Apply Isochromatic Unwrap", value=False)


if uploaded_files:
    if len(uploaded_files) >= 10 and calculate_phase:
        if image_dict_cropped:
            images = image_dict_cropped
        else:
            images = image_dict
        # Calculate phases
        iso_phase = isoclinic_phase(
            images['I1'], images['I2'], 
            images['I3'], images['I4'],
            method=phase_method)
        
        # Unwrap isoclinic phase
        if apply_isoclinic_unwrap:
            iso_phase = np.unwrap(iso_phase, axis=0)
            iso_phase = np.unwrap(iso_phase, axis=1)
        
        # Calculate isochromatic phase
        isochrom_phase = isochromatic_phase(
            iso_phase,
            images['I5'], images['I6'],
            images['I7'], images['I8'],
            images['I9'], images['I10'],
            method=phase_method
        )
        
        # Unwrap isochromatic phase
        if apply_isochromatic_unwrap:
            isochrom_phase = np.unwrap(isochrom_phase, axis=0)
            isochrom_phase = np.unwrap(isochrom_phase, axis=1)


        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Isoclinic Phase")
            color_range = st.slider("Phase Color Range", 
                                    value=(float(np.min(iso_phase)), 
                                           float(np.max(iso_phase))),
                                    key="iso_phase_color_range")
            fig = create_plotly_figure(iso_phase, title=" ", cmap=phase_cmap, color_range=color_range)
            st.plotly_chart(fig)
            if st.button("Save Isoclinic Phase"):
                np.save(f"isoclinic_phase_{iso_phase.shape[0]}_{iso_phase.shape[1]}.npy", iso_phase)
            
        with col2:
            st.subheader("Isochromatic Phase")
            color_range = st.slider("Phase Color Range", 
                                    value=(float(np.min(isochrom_phase)), 
                                           float(np.max(isochrom_phase))),
                                    key="isochrom_phase_color_range")
            fig = create_plotly_figure(isochrom_phase, title=" ", cmap=phase_cmap, color_range=color_range)
            st.plotly_chart(fig)
            if st.button("Save Isochromatic Phase"):
                np.save(f"isochrom_phase_{isochrom_phase.shape[0]}_{isochrom_phase.shape[1]}.npy", isochrom_phase)

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.session_state.do_compress_image = st.checkbox("Compress Image", value=st.session_state.do_compress_image)
        with col2:
            skip_points = st.number_input("Skip Points", value=3, min_value=1, max_value=10, step=1)
        if st.session_state.do_compress_image:
            # compressed_image = compress_image_with_gaussian(iso_phase, kernel_size=3, sigma=1.0, jpeg_quality=50, scale_factor=0.5)
            compressed_image = compress_image(iso_phase, skip_points=skip_points)
            color_range = st.slider("Phase Color Range", 
                                    value=(float(np.min(compressed_image)), 
                                           float(np.max(compressed_image))),
                                    key="compressed_image_color_range")
            fig = create_plotly_figure(compressed_image, title="Compressed Image", cmap=colormap, color_range=color_range)
            st.plotly_chart(fig)
        if st.session_state.do_compress_image:
            
            # Create download button
            if st.button("Save Compressed Image Data"):
                np.save(f"compressed_image_{compressed_image.shape[0]}_{compressed_image.shape[1]}.npy", compressed_image)
        
        # create_quiver_plot = st.checkbox("Isoclinic Phase Quiver Plot", value=False)
        # if create_quiver_plot:
        #     quiver_fig = quiver_plot_matplotlib(compressed_image, scale=1)
        #     st.pyplot(quiver_fig)

    else:
        st.warning("Please upload all 10 images (I1-I10)")
else:
    st.info("Upload your images to begin analysis")

