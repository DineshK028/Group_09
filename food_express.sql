-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 12, 2026 at 10:10 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `food_express`
--

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `cart_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `restaurant_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`cart_id`, `user_id`, `restaurant_id`) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 3);

-- --------------------------------------------------------

--
-- Table structure for table `cart_items`
--

CREATE TABLE `cart_items` (
  `cart_item_id` int(11) NOT NULL,
  `cart_id` int(11) DEFAULT NULL,
  `item_id` int(11) DEFAULT NULL,
  `quantity` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart_items`
--

INSERT INTO `cart_items` (`cart_item_id`, `cart_id`, `item_id`, `quantity`) VALUES
(1, 1, 1, 2),
(2, 1, 2, 1),
(3, 1, 3, 3),
(4, 2, 5, 1),
(5, 2, 6, 1),
(6, 2, 7, 4),
(7, 3, 9, 1),
(8, 3, 10, 1),
(9, 3, 12, 2);

-- --------------------------------------------------------

--
-- Table structure for table `delivery_assignments`
--

CREATE TABLE `delivery_assignments` (
  `assignment_id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `delivery_user_id` int(11) DEFAULT NULL,
  `status` varchar(20) NOT NULL DEFAULT 'accepted',
  `assigned_at` datetime NOT NULL DEFAULT current_timestamp(),
  `accepted_at` datetime DEFAULT NULL,
  `picked_at` datetime DEFAULT NULL,
  `delivered_at` datetime DEFAULT NULL,
  `rejected_at` datetime DEFAULT NULL,
  `notes` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `delivery_assignments`
--

INSERT INTO `delivery_assignments` (`assignment_id`, `order_id`, `delivery_user_id`, `status`, `assigned_at`, `accepted_at`, `picked_at`, `delivered_at`, `rejected_at`, `notes`) VALUES
(1, 1, 10, 'delivered', '2026-07-09 12:30:00', '2026-07-09 12:32:00', '2026-07-09 12:50:00', '2026-07-09 13:20:00', NULL, 'Delivered successfully, OTP verified'),
(2, 2, 11, 'picked', '2026-07-09 13:20:00', '2026-07-09 13:22:00', '2026-07-09 13:40:00', NULL, NULL, 'Customer prefers contactless delivery'),
(3, 3, 12, 'accepted', '2026-07-09 13:50:00', '2026-07-09 13:52:00', NULL, NULL, NULL, 'Restaurant still preparing order'),
(4, 5, 11, 'assigned', '2026-07-09 14:10:00', NULL, NULL, NULL, NULL, 'Awaiting delivery person confirmation');

-- --------------------------------------------------------

--
-- Table structure for table `delivery_events`
--

CREATE TABLE `delivery_events` (
  `id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `delivery_person_id` int(11) DEFAULT NULL,
  `event_type` varchar(50) NOT NULL,
  `event_time` datetime NOT NULL DEFAULT current_timestamp(),
  `meta` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`meta`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `delivery_events`
--

INSERT INTO `delivery_events` (`id`, `order_id`, `delivery_person_id`, `event_type`, `event_time`, `meta`) VALUES
(1, 1, 10, 'assigned', '2026-07-09 12:30:00', '{\"note\": \"Delivery assigned to Amit Verma\"}'),
(2, 1, 10, 'picked_up', '2026-07-09 12:50:00', '{\"location\": \"Spice Garden\"}'),
(3, 1, 10, 'out_for_delivery', '2026-07-09 13:00:00', '{\"location\": \"MG Road\"}'),
(4, 1, 10, 'delivered', '2026-07-09 13:20:00', '{\"otp_verified\": true}'),
(5, 2, 11, 'assigned', '2026-07-09 13:20:00', '{\"note\": \"Delivery assigned to Neha Kapoor\"}'),
(6, 2, 11, 'picked_up', '2026-07-09 13:40:00', '{\"location\": \"Lucknowi Zaika\"}'),
(7, 2, 11, 'out_for_delivery', '2026-07-09 14:00:00', '{\"location\": \"MG Road\"}'),
(8, 3, 12, 'assigned', '2026-07-09 13:50:00', '{\"note\": \"Delivery assigned to Rajesh Yadav\"}'),
(9, 4, NULL, 'cancelled', '2026-07-09 12:45:00', '{\"reason\": \"Customer requested cancellation\"}'),
(10, 5, NULL, 'order_confirmed', '2026-07-09 14:10:00', '{\"note\": \"Awaiting delivery assignment\"}');

-- --------------------------------------------------------

--
-- Table structure for table `delivery_persons`
--

CREATE TABLE `delivery_persons` (
  `delivery_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `vehicle_type` varchar(50) DEFAULT NULL,
  `vehicle_number` varchar(50) DEFAULT NULL,
  `license_number` varchar(50) DEFAULT NULL,
  `rating` decimal(3,2) DEFAULT 0.00,
  `total_deliveries` int(11) DEFAULT 0,
  `total_earnings` decimal(10,2) DEFAULT 0.00,
  `availability` enum('available','on_break','offline') DEFAULT 'available'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `delivery_persons`
--

INSERT INTO `delivery_persons` (`delivery_id`, `user_id`, `vehicle_type`, `vehicle_number`, `license_number`, `rating`, `total_deliveries`, `total_earnings`, `availability`) VALUES
(1, 10, 'Motorbike', 'KA05AB1234', 'LICKA123456', 4.70, 320, 158000.00, 'available'),
(2, 11, 'Scooter', 'MH12XY9876', 'LICMH987654', 4.50, 210, 102500.00, 'on_break'),
(3, 12, 'Bicycle', 'DL01BC4321', 'LICDL456789', 4.30, 150, 75000.00, 'offline');

-- --------------------------------------------------------

--
-- Table structure for table `menu_categories`
--

CREATE TABLE `menu_categories` (
  `category_id` int(11) NOT NULL,
  `restaurant_id` int(11) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu_categories`
--

INSERT INTO `menu_categories` (`category_id`, `restaurant_id`, `name`, `description`) VALUES
(1, 1, 'Starters', 'A variety of Indian appetizers including samosas, pakoras, and kebabs.'),
(2, 1, 'Main Course', 'Traditional Indian curries, biryanis, and tandoori dishes.'),
(3, 1, 'Desserts', 'Indian sweets like gulab jamun, rasmalai, and kheer.'),
(4, 1, 'Beverages', 'Fresh juices, lassi, masala chai, and soft drinks.'),
(5, 2, 'Starters', 'Mughlai kebabs, tikkas, and shami kebabs.'),
(6, 2, 'Main Course', 'Rich Mughlai curries, biryanis, and koftas.'),
(7, 2, 'Breads', 'Variety of naan, paratha, and roomali roti.'),
(8, 2, 'Desserts', 'Shahi tukda, phirni, and kulfi.'),
(9, 3, 'Starters', 'Paneer tikka, hara bhara kebab, and tandoori mushrooms.'),
(10, 3, 'Main Course', 'North Indian curries, dal makhani, and butter chicken.'),
(11, 3, 'Breads', 'Tandoori roti, butter naan, and missi roti.'),
(12, 3, 'Beverages', 'Sweet lassi, salted lassi, and masala chai.');

-- --------------------------------------------------------

--
-- Table structure for table `menu_items`
--

CREATE TABLE `menu_items` (
  `item_id` int(11) NOT NULL,
  `restaurant_id` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `price` decimal(6,2) NOT NULL,
  `quantity` int(11) NOT NULL,
  `discount_price` decimal(6,2) DEFAULT NULL,
  `ingredients` text NOT NULL,
  `is_vegetarian` tinyint(1) DEFAULT 0,
  `is_spicy` tinyint(1) DEFAULT 0,
  `is_available` tinyint(1) DEFAULT 1,
  `preparation_time` int(11) DEFAULT NULL,
  `rating` decimal(3,2) DEFAULT 0.00,
  `total_orders` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu_items`
--

INSERT INTO `menu_items` (`item_id`, `restaurant_id`, `category_id`, `name`, `description`, `price`, `quantity`, `discount_price`, `ingredients`, `is_vegetarian`, `is_spicy`, `is_available`, `preparation_time`, `rating`, `total_orders`) VALUES
(1, 1, 1, 'Paneer Tikka', 'Grilled cottage cheese cubes marinated in Indian spices.', 180.00, 50, 150.00, 'Paneer, yogurt, spices', 1, 1, 1, 20, 4.50, 120),
(2, 1, 2, 'Chicken Biryani', 'Fragrant basmati rice cooked with chicken and spices.', 250.00, 40, 220.00, 'Chicken, rice, spices', 0, 1, 1, 30, 4.70, 200),
(3, 1, 3, 'Gulab Jamun', 'Soft fried dumplings soaked in sugar syrup.', 90.00, 60, NULL, 'Milk solids, sugar, cardamom', 1, 0, 1, 10, 4.60, 150),
(4, 1, 4, 'Masala Chai', 'Traditional Indian spiced tea.', 40.00, 100, NULL, 'Tea leaves, milk, spices', 1, 1, 1, 5, 4.40, 300),
(5, 2, 5, 'Galouti Kebab', 'Melt-in-mouth minced meat kebabs.', 220.00, 30, 200.00, 'Minced meat, spices', 0, 1, 1, 25, 4.80, 180),
(6, 2, 6, 'Mutton Rogan Josh', 'Slow-cooked mutton curry with aromatic spices.', 300.00, 25, NULL, 'Mutton, spices, yogurt', 0, 1, 1, 35, 4.70, 140),
(7, 2, 7, 'Butter Naan', 'Soft leavened bread with butter.', 50.00, 80, NULL, 'Flour, butter, yeast', 1, 0, 1, 8, 4.50, 250),
(8, 2, 8, 'Shahi Tukda', 'Rich bread pudding with saffron milk.', 120.00, 40, NULL, 'Bread, milk, sugar, saffron', 1, 0, 1, 15, 4.60, 100),
(9, 3, 9, 'Hara Bhara Kebab', 'Spinach and green pea patties.', 150.00, 40, 130.00, 'Spinach, peas, spices', 1, 0, 1, 15, 4.40, 110),
(10, 3, 10, 'Butter Chicken', 'Creamy tomato-based chicken curry.', 280.00, 35, 250.00, 'Chicken, cream, tomatoes, spices', 0, 0, 1, 25, 4.80, 210),
(11, 3, 11, 'Tandoori Roti', 'Whole wheat flatbread cooked in tandoor.', 30.00, 100, NULL, 'Whole wheat flour, water, salt', 1, 0, 1, 5, 4.30, 300),
(12, 3, 12, 'Sweet Lassi', 'Sweetened yogurt drink.', 60.00, 70, NULL, 'Yogurt, sugar, cardamom', 1, 0, 1, 5, 4.50, 180);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `restaurant_id` int(11) DEFAULT NULL,
  `delivery_person_id` int(11) DEFAULT NULL,
  `order_number` varchar(20) NOT NULL,
  `total_amount` decimal(8,2) NOT NULL,
  `discount_amount` decimal(6,2) DEFAULT 0.00,
  `final_amount` decimal(8,2) NOT NULL,
  `delivery_address` text NOT NULL,
  `delivery_instruction` text DEFAULT NULL,
  `payment_method` enum('credit_card','debit_card','COD','wallet') DEFAULT 'credit_card',
  `payment_status` enum('pending','paid','failed','refunded') DEFAULT 'pending',
  `order_status` enum('pending','accepted','out_for_delivery','delivered','c\r\nancelled') NOT NULL DEFAULT 'pending',
  `estimated_delivery_time` datetime DEFAULT NULL,
  `actual_delivery_time` datetime DEFAULT NULL,
  `decline_reason` varchar(255) DEFAULT NULL,
  `picked_up_at` datetime DEFAULT NULL,
  `delivered_at` datetime DEFAULT NULL,
  `delivery_otp` varchar(6) DEFAULT NULL,
  `pod_photo` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`order_id`, `user_id`, `restaurant_id`, `delivery_person_id`, `order_number`, `total_amount`, `discount_amount`, `final_amount`, `delivery_address`, `delivery_instruction`, `payment_method`, `payment_status`, `order_status`, `estimated_delivery_time`, `actual_delivery_time`, `decline_reason`, `picked_up_at`, `delivered_at`, `delivery_otp`, `pod_photo`) VALUES
(1, 1, 1, 10, 'ORD1001', 500.00, 50.00, 450.00, '12 MG Road, Bengaluru, 560015', 'Leave at the door', 'credit_card', 'paid', 'delivered', '2026-07-09 13:00:00', '2026-07-09 13:20:00', NULL, '2026-07-09 12:50:00', '2026-07-09 13:20:00', '123456', 'pod1.jpg'),
(2, 2, 2, 11, 'ORD1002', 750.00, 0.00, 750.00, '45 MG Road, Bengaluru, 560234', 'Call on arrival', 'COD', 'pending', 'out_for_delivery', '2026-07-09 14:00:00', NULL, NULL, '2026-07-09 13:40:00', NULL, '654321', NULL),
(3, 3, 3, 12, 'ORD1003', 320.00, 20.00, 300.00, '45 Park Street, Kolkata, 700016', 'Ring the bell twice', 'wallet', 'paid', 'pending', '2026-07-09 14:30:00', NULL, NULL, NULL, NULL, '789012', NULL),
(4, 1, 2, NULL, 'ORD1004', 600.00, 0.00, 600.00, '12 MG Road, Bengaluru, 560015', 'No onions please', 'debit_card', 'refunded', '', NULL, NULL, 'Customer requested cancellation', NULL, NULL, NULL, NULL),
(5, 2, 1, NULL, 'ORD1005', 450.00, 30.00, 420.00, '45 MG Road, Bengaluru, 560234', 'Extra spicy', 'credit_card', 'paid', 'accepted', '2026-07-09 15:00:00', NULL, NULL, NULL, NULL, '345678', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `order_item_id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `item_id` int(11) DEFAULT NULL,
  `quantity` int(11) NOT NULL DEFAULT 1,
  `unit_price` decimal(6,2) NOT NULL,
  `item_total` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`order_item_id`, `order_id`, `item_id`, `quantity`, `unit_price`, `item_total`) VALUES
(1, 1, 1, 2, 180.00, NULL),
(2, 1, 2, 1, 250.00, NULL),
(3, 1, 3, 3, 90.00, NULL),
(4, 2, 5, 2, 220.00, NULL),
(5, 2, 6, 1, 300.00, NULL),
(6, 2, 7, 4, 50.00, NULL),
(7, 3, 9, 1, 150.00, NULL),
(8, 3, 10, 1, 280.00, NULL),
(9, 3, 11, 3, 30.00, NULL),
(10, 3, 12, 2, 60.00, NULL),
(11, 4, 5, 1, 220.00, NULL),
(12, 4, 8, 2, 120.00, NULL),
(13, 5, 1, 1, 180.00, NULL),
(14, 5, 4, 2, 40.00, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `payment_id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `transaction_id` varchar(100) DEFAULT NULL,
  `payment_method` enum('credit_card','debit_card','COD','wallet') DEFAULT NULL,
  `amount` decimal(8,2) NOT NULL,
  `payment_status` enum('pending','completed','failed','refunded') DEFAULT 'pending',
  `payment_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `gateway_response` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`payment_id`, `order_id`, `transaction_id`, `payment_method`, `amount`, `payment_status`, `payment_date`, `gateway_response`) VALUES
(1, 1, 'TXN1001CC', 'credit_card', 450.00, 'completed', '2026-09-12 20:08:39', '{\"status\":\"success\",\"auth_code\":\"AUTH123\",\"message\":\"Payment approved\"}'),
(2, 2, 'TXN1002COD', 'COD', 750.00, 'pending', '2026-09-12 20:08:39', '{\"status\":\"pending\",\"message\":\"Cash to be collected on delivery\"}'),
(3, 3, 'TXN1003WAL', 'wallet', 300.00, 'completed', '2026-09-12 20:08:39', '{\"status\":\"success\",\"wallet_id\":\"WALLET567\",\"message\":\"Wallet payment successful\"}'),
(4, 4, 'TXN1004DC', 'debit_card', 600.00, 'refunded', '2026-09-12 20:08:39', '{\"status\":\"refunded\",\"refund_id\":\"REF123\",\"message\":\"Amount refunded to card\"}'),
(5, 5, 'TXN1005CC', 'credit_card', 420.00, 'completed', '2026-09-12 20:08:39', '{\"status\":\"success\",\"auth_code\":\"AUTH789\",\"message\":\"Payment approved\"}');

-- --------------------------------------------------------

--
-- Table structure for table `restaurants`
--

CREATE TABLE `restaurants` (
  `restaurant_id` int(11) NOT NULL,
  `owner_id` int(11) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `cuisine_type` varchar(50) NOT NULL,
  `address` text NOT NULL,
  `city` varchar(50) NOT NULL,
  `zip_code` varchar(20) DEFAULT NULL,
  `contact_phone` varchar(15) NOT NULL,
  `contact_email` varchar(50) NOT NULL,
  `opening_time` time DEFAULT '10:00:00',
  `closing_time` time DEFAULT '22:00:00',
  `is_open` tinyint(1) DEFAULT 1,
  `delivery_fee` decimal(6,2) DEFAULT 15.00,
  `minimum_order` decimal(6,2) DEFAULT 100.00,
  `rating` decimal(3,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `restaurants`
--

INSERT INTO `restaurants` (`restaurant_id`, `owner_id`, `name`, `cuisine_type`, `address`, `city`, `zip_code`, `contact_phone`, `contact_email`, `opening_time`, `closing_time`, `is_open`, `delivery_fee`, `minimum_order`, `rating`) VALUES
(1, 4, 'Kings gardenia', 'Indian', '22 Civil Lines', 'Bengaluru', '560013', '9876544444', 'kingsgardenia@food.com', '10:00:00', '22:00:00', 1, 20.00, 150.00, 4.50),
(2, 5, 'RRR Restaurant', 'Mughlai', '44 GM Road', 'Mysore', '226022', '9876522222', 'rrrrestaurant@food.com', '11:00:00', '23:00:00', 1, 25.00, 200.00, 4.20),
(3, 3, 'Nandhana Palace', 'North Indian', '13 Laxmi Road', 'Chennai', '300980', '9876511111', 'nandhanapalace@food.com', '09:30:00', '21:30:00', 1, 15.00, 120.00, 4.00);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `user_type` enum('Customer','Restaurant_Owner','Admin','Delivery_Person') DEFAULT 'Customer',
  `address` text NOT NULL,
  `city` varchar(50) NOT NULL,
  `zip_code` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `email`, `password_hash`, `phone`, `user_type`, `address`, `city`, `zip_code`) VALUES
(1, 'Pallavi', 'pallavi@infy.com', 'Pallavi@456', '9876543210', 'Customer', '14 MG Road', 'Bengaluru', '560015'),
(2, 'Lavanya', 'lavanya@infy.com', 'Lavanya@123', '9876512345', 'Customer', '48 MG Road', 'Bengaluru', '560234'),
(3, 'Mahesh R', 'mahesh@infy.com', 'Mahesh@345', '9876987600', 'Restaurant_Owner', '45 Park Street', 'Kolkata', '700016'),
(4, 'Shiksha', 'shiksha@infy.com', 'Shiksha@123', '8867251052', 'Delivery_Person', '163 Manglore', 'Udupi', '560234'),
(5, 'Rohit Sharma', 'rohit@infy.com', '12345hello', '9876544444', 'Restaurant_Owner', '22 Civil Lines', 'Bengaluru', '560013'),
(6, 'Vikas A', 'vikas@infy.com', '12ab12', '9876522222', 'Restaurant_Owner', '22 GM Road', 'Lucknow', '226022'),
(7, 'Arjun Patel', 'arjun@infy.com', 'hello54321', '9876511111', 'Restaurant_Owner', '13 Laxmi Road', 'Ahemdabad', '300980'),
(8, 'Anil Kumar', 'anil.admin@infy.com', 'admin123', '9000000001', 'Admin', '101 Admin Block', 'Bengaluru', '560001'),
(9, 'Priya Singh', 'priya.admin@infy.com', 'admin456', '9000000002', 'Admin', '202 Admin Block', 'Mumbai', '400001'),
(10, 'Ramesh Gupta', 'ramesh.admin@infy.com', 'admin789', '9000000003', 'Admin', '303 Admin Block', 'Delhi', '110001'),
(11, 'Amit Verma', 'amit.delivery@infy.com', 'del123', '9111111111', 'Delivery_Person', '12 Delivery Lane', 'Bengaluru', '560002'),
(12, 'Neha Kapoor', 'neha.delivery@infy.com', 'del456', '9222222222', 'Delivery_Person', '34 Delivery Lane', 'Mumbai', '400002'),
(13, 'Rajesh Yadav', 'rajesh.delivery@infy.com', 'del789', '9333333333', 'Delivery_Person', '56 Delivery Lane', 'Delhi', '110002');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`cart_id`),
  ADD UNIQUE KEY `uk_user_id` (`user_id`),
  ADD KEY `restaurant_id` (`restaurant_id`);

--
-- Indexes for table `cart_items`
--
ALTER TABLE `cart_items`
  ADD PRIMARY KEY (`cart_item_id`),
  ADD UNIQUE KEY `uk_cart_item` (`cart_id`,`item_id`),
  ADD KEY `item_id` (`item_id`);

--
-- Indexes for table `delivery_assignments`
--
ALTER TABLE `delivery_assignments`
  ADD PRIMARY KEY (`assignment_id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `delivery_user_id` (`delivery_user_id`);

--
-- Indexes for table `delivery_events`
--
ALTER TABLE `delivery_events`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `delivery_person_id` (`delivery_person_id`);

--
-- Indexes for table `delivery_persons`
--
ALTER TABLE `delivery_persons`
  ADD PRIMARY KEY (`delivery_id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `menu_categories`
--
ALTER TABLE `menu_categories`
  ADD PRIMARY KEY (`category_id`),
  ADD KEY `restaurant_id` (`restaurant_id`);

--
-- Indexes for table `menu_items`
--
ALTER TABLE `menu_items`
  ADD PRIMARY KEY (`item_id`),
  ADD KEY `restaurant_id` (`restaurant_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD UNIQUE KEY `order_number` (`order_number`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `restaurant_id` (`restaurant_id`),
  ADD KEY `delivery_person_id` (`delivery_person_id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`order_item_id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `item_id` (`item_id`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`payment_id`),
  ADD UNIQUE KEY `uk_transaction_id` (`transaction_id`),
  ADD KEY `order_id` (`order_id`);

--
-- Indexes for table `restaurants`
--
ALTER TABLE `restaurants`
  ADD PRIMARY KEY (`restaurant_id`),
  ADD UNIQUE KEY `contact_email` (`contact_email`),
  ADD KEY `owner_id` (`owner_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `phone` (`phone`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `cart_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `cart_items`
--
ALTER TABLE `cart_items`
  MODIFY `cart_item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `delivery_assignments`
--
ALTER TABLE `delivery_assignments`
  MODIFY `assignment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `delivery_events`
--
ALTER TABLE `delivery_events`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `delivery_persons`
--
ALTER TABLE `delivery_persons`
  MODIFY `delivery_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `menu_categories`
--
ALTER TABLE `menu_categories`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `menu_items`
--
ALTER TABLE `menu_items`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `order_item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `payment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `restaurants`
--
ALTER TABLE `restaurants`
  MODIFY `restaurant_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurants` (`restaurant_id`) ON DELETE SET NULL;

--
-- Constraints for table `cart_items`
--
ALTER TABLE `cart_items`
  ADD CONSTRAINT `cart_items_ibfk_1` FOREIGN KEY (`cart_id`) REFERENCES `cart` (`cart_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `cart_items_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `menu_items` (`item_id`) ON DELETE CASCADE;

--
-- Constraints for table `delivery_assignments`
--
ALTER TABLE `delivery_assignments`
  ADD CONSTRAINT `delivery_assignments_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `delivery_assignments_ibfk_2` FOREIGN KEY (`delivery_user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `delivery_events`
--
ALTER TABLE `delivery_events`
  ADD CONSTRAINT `delivery_events_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `delivery_events_ibfk_2` FOREIGN KEY (`delivery_person_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `delivery_persons`
--
ALTER TABLE `delivery_persons`
  ADD CONSTRAINT `delivery_persons_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `menu_categories`
--
ALTER TABLE `menu_categories`
  ADD CONSTRAINT `menu_categories_ibfk_1` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurants` (`restaurant_id`) ON DELETE CASCADE;

--
-- Constraints for table `menu_items`
--
ALTER TABLE `menu_items`
  ADD CONSTRAINT `menu_items_ibfk_1` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurants` (`restaurant_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `menu_items_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `menu_categories` (`category_id`) ON DELETE SET NULL;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurants` (`restaurant_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`delivery_person_id`) REFERENCES `users` (`user_id`) ON DELETE SET NULL;

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `menu_items` (`item_id`) ON DELETE SET NULL;

--
-- Constraints for table `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE;

--
-- Constraints for table `restaurants`
--
ALTER TABLE `restaurants`
  ADD CONSTRAINT `restaurants_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
