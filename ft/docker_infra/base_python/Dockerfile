ARG base_node_js_latest_tag
FROM base_node_js:${base_node_js_latest_tag}

RUN apt-get install -y --no-install-recommends \
    python3 \
    python3-pip

RUN pip3 install nibabel pydicom matplotlib pillow
RUN pip3 install med2image

