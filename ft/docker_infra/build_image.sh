log_file="`pwd`/logs/build_`date +%Y%m%d_%H%M%S`.log"
sudo echo "***** logs at $log_file"
cd base_os
export base_os_latest_tag=0.0.1
sudo docker build --progress=plain --tag base_os:$base_os_latest_tag . 2>&1 | tee -a $log_file
cd -
cd base_node_js
export base_node_js_latest_tag=0.0.1
sudo docker build  --progress=plain  --tag base_node_js:$base_node_js_latest_tag . 2>&1 | tee -a $log_file
cd -
cd base_python
export base_python_latest_tag=0.0.1
sudo docker build  --progress=plain   --build-arg base_node_js_latest_tag=$base_node_js_latest_tag --tag base_python:$base_python_latest_tag . 2>&1 | tee -a $log_file
cd -


cd flat_trade_token_generator 
export flat_trade_token_generator_latest_tag=0.0.1
sudo docker build  --progress=plain   --build-arg base_python_latest_tag=$base_python_latest_tag --tag flat_trade_token_generator:$flat_trade_token_generator_latest_tag  . 2>&1 | tee -a $log_file
cd -

echo "***** logs at $log_file"
