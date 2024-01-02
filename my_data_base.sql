
CREATE TABLE `garage`.`cars` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `model` INT NULL,
  `brand` VARCHAR(25) NULL,
  `color` VARCHAR(10) NULL,
  PRIMARY KEY (`id`));

-- bla bla
SELECT `cars`.`id`,
    `cars`.`model`,
    `cars`.`brand`,
    `cars`.`color`
FROM `garage`.`cars`
where color ='red'
;

INSERT INTO `cars` (`model`, `brand`,`color`)  VALUES  (-1,"kia","red");


DELETE FROM `garage`.`cars` WHERE color='red';

UPDATE `garage`.`cars`
SET
`model` = 222,
`brand` = "vovo",
`color` = "gold"
WHERE `id` =2;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);
