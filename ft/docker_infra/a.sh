log_file="`pwd`/logs/build_`date +%Y%m%d_%H%M%S`.log"
sudo echo "***** logs at $log_file"
export base_python_latest_tag=0.0.1
cd flat_trade_token_generator 
export flat_trade_token_generator_latest_tag=0.0.1
sudo docker build  --progress=plain   --build-arg base_python_latest_tag=$base_python_latest_tag --tag flat_trade_token_generator:$flat_trade_token_generator_latest_tag  . 2>&1 | tee -a $log_file
cd -

echo "***** logs at $log_file"
