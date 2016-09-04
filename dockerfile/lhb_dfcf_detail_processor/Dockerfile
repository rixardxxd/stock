FROM index.alauda.cn/palmorg/scrapy_alpine

MAINTAINER palmscience <contact@palm.science>

# Add and install Python modules
ADD requirements.txt stock/requirements.txt
RUN cd /stock; pip3 install -r requirements.txt

# Bundle app source
ADD scrapy.cfg stock/scrapy.cfg
ADD crawler stock/crawler
ADD my_scrapy_redis stock/my_scrapy_redis
ADD config stock/config
ADD utils stock/utils
ADD processor stock/processor

# Expose
EXPOSE 5000

# Run scrapy
CMD cd stock; python3 -m processor.lhb.lhb_detail_dfcf_processor