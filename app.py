import streamlit as st
import numpy as np
from pathlib import Path
from modules.image_process import png_to_array, crop_image
from modules.plotting_modules import create_plotly_figure, heatmap_plot_with_bounding_box
from analysis import isoclinic_phase, isochromatic_phase

st.set_page_config(page_title="Stress Imaging Analysis", layout="wide")
st.title("Stress Imaging Analysis")

# Sidebar controls
st.sidebar.header("Analysis Settings")
phase_method = st.sidebar.selectbox(
    "Phase Calculation Method",
    ["arctan2", "arctan"],
    help="Method used to calculate phase angles"
)

# calibration_file = st.sidebar.file_uploader("Upload Calibration File", 
#                                             type=['png', 'jpg', 'jpeg'])

# File upload section
st.header("Image Upload")
uploaded_files = st.file_uploader(
    "Upload images (I1-I10)", 
    accept_multiple_files=True,
    type=['png', 'jpg', 'jpeg']
)

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
        do_cropping = st.checkbox("Apply Cropping to all images", value=True)
        show_full_images = st.checkbox("Show Full Images", value=False)
        if do_cropping:
            show_cropped_images = st.checkbox("Show Cropped Images", value=True)

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
    for idx, file in enumerate(uploaded_files):
        name = file.name.split('.')[0].upper()  # Get filename without extension
        image_array = png_to_array(file)
        image_dict[name] = image_array
        if do_cropping:
            image_array_cropped = crop_image(image_array, crop_range_x, crop_range_y)
            image_dict[f"{name}_cropped"] = image_array_cropped
        
        # Create plotly figure
        with st.expander(f"{name} Colormap", expanded=False):
            color_range = st.slider("Color Range", 
                                            min_value=0.0, 
                                            max_value=65000.0, 
                                            value=(float(np.min(image_dict[name])), float(np.max(image_dict[name]))),
                                            key=f"{name}_color_range")
            # fig = create_plotly_figure(image_dict[name], title=f"{name}", color_range=color_range, cmap=colormap)
            if show_full_images:
                fig = heatmap_plot_with_bounding_box(image_dict[name], 
                                                title=f"{name}", 
                                                color_map=colormap, 
                                                color_range=color_range,
                                                fig_height=800,
                                                fig_width=800,
                                                bounding_box=bounding_box)
                st.plotly_chart(fig)
            if do_cropping and show_cropped_images:
                fig_cropped = create_plotly_figure(image_dict[f"{name}_cropped"], 
                                                title=f"{name} Cropped", 
                                                cmap=colormap, 
                                                color_range=color_range)
                st.plotly_chart(fig_cropped)
    
#     if len(image_dict) >= 10:  # Check if we have all required images
#         # Calculate phases
#         iso_phase = isoclinic_phase(
#             image_dict['I1'], image_dict['I2'], 
#             image_dict['I3'], image_dict['I4'],
#             method=phase_method
#         )
        
#         # Unwrap isoclinic phase
#         iso_phase_unwrap = np.unwrap(iso_phase, axis=0)
#         iso_phase_unwrap = np.unwrap(iso_phase_unwrap, axis=1)
        
#         # Calculate isochromatic phase
#         isochrom_phase = isochromatic_phase(
#             iso_phase,
#             image_dict['I5'], image_dict['I6'],
#             image_dict['I7'], image_dict['I8'],
#             image_dict['I9'], image_dict['I10'],
#             method=phase_method
#         )
        
#         # Display results
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.subheader("Isoclinic Phase")
#             st.image(iso_phase_unwrap, caption="Unwrapped Isoclinic Phase", use_column_width=True)
            
#         with col2:
#             st.subheader("Isochromatic Phase")
#             st.image(isochrom_phase, caption="Isochromatic Phase", use_column_width=True)
            
#     else:
#         st.warning("Please upload all 10 images (I1-I10)")
# else:
#     st.info("Upload your images to begin analysis")
