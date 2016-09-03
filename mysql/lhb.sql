CREATE TABLE `lhb_summary` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `stock_id` char(20) DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `reason` varchar(100) DEFAULT NULL,
  `change_percent` decimal(5,2) DEFAULT NULL,
  `buy_value` decimal(15,2) DEFAULT NULL,
  `sell_value` decimal(15,2) DEFAULT NULL,
  `net_value` decimal(15,2) DEFAULT NULL,
  `process_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `stock_id_end_date_reason` (`stock_id`,`end_date`,`reason`)
) ENGINE=InnoDB AUTO_INCREMENT=35069 DEFAULT CHARSET=utf8;

CREATE TABLE `lhb_detail` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `stock_id` char(15) DEFAULT NULL,
  `institution_name` int(15) DEFAULT NULL,
  `buy_value` int(15) DEFAULT NULL,
  `buy_over_total_ratio` int(11) DEFAULT NULL,
  `sell_value` int(11) DEFAULT NULL,
  `sell_over_total_ratio` int(11) DEFAULT NULL,
  `net_buy_value` int(11) DEFAULT NULL,
  `trade_detail_url` varchar(100) DEFAULT NULL,
  `reason` char(100) DEFAULT NULL,
  `close_price` float DEFAULT NULL,
  `change_percent` float DEFAULT NULL,
  `total_volume` int(11) DEFAULT NULL,
  `total_amount` int(11) DEFAULT NULL,
  `crawl_date` datetime DEFAULT NULL,
  `process_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `lhb_summary_dfcf` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `lhb_date` date DEFAULT NULL,
  `stock_id` char(6) DEFAULT NULL,
  `stock_name` char(20) DEFAULT NULL,
  `close_price` decimal(5,2) DEFAULT NULL,
  `change_percent` decimal(10,2) DEFAULT NULL,
  `lhb_net_value` decimal(15,2) DEFAULT NULL,
  `lhb_buy_value` decimal(15,2) DEFAULT NULL,
  `lhb_sell_value` decimal(15,2) DEFAULT NULL,
  `lhb_total_value` decimal(15,2) DEFAULT NULL,
  `trade_amount` decimal(15,2) DEFAULT NULL,
  `net_value_percent` decimal(10,2) DEFAULT NULL,
  `total_value_percent` decimal(10,2) DEFAULT NULL,
  `turnover_ratio` decimal(10,2) DEFAULT NULL,
  `reason` varchar(100) DEFAULT NULL,
  `process_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `stock_id_lhb_date_reason` (`stock_id`,`lhb_date`,`reason`)
) ENGINE=InnoDB AUTO_INCREMENT=79840 DEFAULT CHARSET=utf8;

CREATE TABLE `lhb_detail_dfcf` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `lhb_date` date DEFAULT NULL,
  `stock_id` char(6) DEFAULT NULL,
  `stock_name` char(20) DEFAULT NULL,
  `reason` varchar(100) DEFAULT NULL,
  `yyb_name` varchar(100) DEFAULT NULL,
  `buy_or_sell` char(1) DEFAULT NULL,
  `buy_or_sell_order` char(1) DEFAULT NULL,
  `buy_value` decimal(15,2) DEFAULT NULL,
  `buy_value_percent` decimal(8,2) DEFAULT NULL,
  `sell_value` decimal(15,2) DEFAULT NULL,
  `sell_value_percent` decimal(8,2) DEFAULT NULL,
  `net_value` decimal(15,2) DEFAULT NULL,
  `process_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `stock_id_lhb_date_reason_yyb_name_buy_or_sell_order` (`stock_id`,`lhb_date`,`reason`,`yyb_name`,`buy_or_sell`,`buy_or_sell_order`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
