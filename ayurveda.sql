-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 19, 2025 at 12:50 PM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `organic_shop`
--

-- --------------------------------------------------------

--
-- Table structure for table `addproduct`
--

CREATE TABLE `addproduct` (
  `id` int(20) NOT NULL,
  `username` varchar(20) NOT NULL,
  `name` varchar(20) NOT NULL,
  `Description` varchar(300) NOT NULL,
  `Amount` varchar(20) NOT NULL,
  `Type` varchar(20) NOT NULL,
  `image` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `addproduct`
--

INSERT INTO `addproduct` (`id`, `username`, `name`, `Description`, `Amount`, `Type`, `image`) VALUES
(1, '', 'palm sugar', 'Palm sugar is a natural sweetener made from the sap of palm trees', '100', 'Palm', 'p1p12.jpg'),
(2, '', 'Coffee', 'A unique, earthy-flavored coffee blend made from roasted palm seeds,', '200', 'Palm', 'p2p2.jpg'),
(3, 'ram', 'Coffee', 'A unique, earthy-flavored coffee blend made from roasted palm seeds,', '200', 'Palm', 'p3p5.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `id` int(20) NOT NULL,
  `username` varchar(20) NOT NULL,
  `email` varchar(20) NOT NULL,
  `mobile` bigint(10) NOT NULL,
  `address` varchar(30) NOT NULL,
  `district` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `confirmpassword` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`id`, `username`, `email`, `mobile`, `address`, `district`, `password`, `confirmpassword`) VALUES
(1, 'sam', 'sam@gmail.com', 9677874082, 'chatiram', 'Trichy', '1234', '1234');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(20) NOT NULL,
  `username` varchar(20) NOT NULL,
  `retailer` varchar(20) NOT NULL,
  `pid` int(40) NOT NULL,
  `contactnumber` bigint(10) NOT NULL,
  `productname` varchar(20) NOT NULL,
  `Amount` varchar(20) NOT NULL,
  `quantity` varchar(20) NOT NULL,
  `totalamount` varchar(40) NOT NULL,
  `address` varchar(225) NOT NULL,
  `district` varchar(40) NOT NULL,
  `status` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `username`, `retailer`, `pid`, `contactnumber`, `productname`, `Amount`, `quantity`, `totalamount`, `address`, `district`, `status`) VALUES
(1, 'sam', '', 2, 9677874082, 'Coffee', '200', '2', '400', 'chatiram', 'Trichy', 0),
(2, 'sam', 'ram', 3, 9677874082, 'Coffee', '200', '3', '600', 'chatiram', 'Trichy', 1);

-- --------------------------------------------------------

--
-- Table structure for table `retailer_reg`
--

CREATE TABLE `retailer_reg` (
  `id` int(20) NOT NULL,
  `username` varchar(20) NOT NULL,
  `email` varchar(20) NOT NULL,
  `mobile` bigint(10) NOT NULL,
  `address` varchar(40) NOT NULL,
  `district` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  `confirmpassword` varchar(20) NOT NULL,
  `status` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `retailer_reg`
--

INSERT INTO `retailer_reg` (`id`, `username`, `email`, `mobile`, `address`, `district`, `password`, `confirmpassword`, `status`) VALUES
(1, 'ram', 'ram@gmail.com', 9677874082, 'chatiram', 'Trichy', '1234', '1234', 1),
(2, 'jani', 'kalai@gmail.com', 1234567898, 'chatiram', 'Trichy', '1234', '1234', 0);

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `id` int(11) NOT NULL auto_increment,
  `username` varchar(255) NOT NULL,
  `rating` int(11) NOT NULL,
  `review_text` text NOT NULL,
  `created_at` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

--
-- Dumping data for table `reviews`
--

INSERT INTO `reviews` (`id`, `username`, `rating`, `review_text`, `created_at`) VALUES
(6, 'sam', 4, 'All products are Good amazing Shop', '2025-04-14 17:51:51');
