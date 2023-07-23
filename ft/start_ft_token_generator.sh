log_file="ft_token_generator_`date +'%Y%m%d_%H%M%S'`.log"
#docker run -it --rm  -v `pwd`:/app  flat_trade_token_generator:0.0.1 bash -c "bash ft_token_generator_start_cmd.sh" 
docker run --detach --rm  -v `pwd`:/app -e TZ=Asia/Kolkata flat_trade_token_generator:0.0.1 bash -c "bash ft_token_generator_start_cmd.sh" > $log_file 2>&1 
