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