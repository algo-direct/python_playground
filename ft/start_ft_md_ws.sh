log_file="ft_md_`date +'%Y%m%d_%H%M%S'`.log"
docker run --detach --rm  -v `pwd`:/app -e TZ=Asia/Kolkata flat_trade_token_generator:0.0.1 bash -c "node ft_md_ws.js"  > $log_file 2>&1 
#docker run --rm -it  -v `pwd`:/app -e TZ=Asia/Kolkata flat_trade_token_generator:0.0.1 bash -c "node ft_md_ws.js"  

