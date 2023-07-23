log_file="x_`date +'%Y%m%d_%H%M%S'`.log"
#docker run --detach --rm  -v `pwd`:/app -e TZ=Asia/Kolkata flat_trade_token_generator:0.0.1 bash -c "node x.js"  > $log_file 2>&1 
docker run --rm -it  -v `pwd`:/app -e TZ=Asia/Kolkata flat_trade_token_generator:0.0.1 bash -c "node x.js"  

