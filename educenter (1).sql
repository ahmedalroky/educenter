-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 10, 2023 at 02:11 PM
-- Server version: 10.4.8-MariaDB
-- PHP Version: 7.3.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `educenter`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(22) NOT NULL,
  `name` varchar(99) NOT NULL,
  `email` varchar(99) NOT NULL,
  `password` varchar(99) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`id`, `name`, `email`, `password`) VALUES
(1, 'admin', 'johndoe@example.com', '12021995'),
(5, 'alroky', 'alroky@icloud.com', '1202195');

-- --------------------------------------------------------

--
-- Table structure for table `classes`
--

CREATE TABLE `classes` (
  `id` int(11) NOT NULL,
  `subject` varchar(100) NOT NULL,
  `day` enum('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday') DEFAULT NULL,
  `time` time DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `teacher_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `classes`
--

INSERT INTO `classes` (`id`, `subject`, `day`, `time`, `location`, `teacher_id`) VALUES
(1, 'Calculus I', 'Monday', '10:00:00', 'Room 101', 1),
(2, 'English Literature', 'Tuesday', '11:00:00', 'Room 102', 2),
(3, 'Math', 'Monday', '09:00:00', 'Room 101', 3);

-- --------------------------------------------------------

--
-- Table structure for table `enrollment`
--

CREATE TABLE `enrollment` (
  `id` int(11) NOT NULL,
  `student_id` int(11) DEFAULT NULL,
  `class_id` int(11) DEFAULT NULL,
  `enrollment_date` date DEFAULT NULL,
  `grade` varchar(10) DEFAULT NULL,
  `exam_score` int(11) DEFAULT NULL,
  `homework_score` int(11) DEFAULT NULL,
  `enrollment_type` enum('exam','homework') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `enrollment`
--

INSERT INTO `enrollment` (`id`, `student_id`, `class_id`, `enrollment_date`, `grade`, `exam_score`, `homework_score`, `enrollment_type`) VALUES
(1, 1, 2, '2023-04-01', 'D', 90, 85, 'exam'),
(2, 2, 2, '2023-04-01', 'C', 90, 85, 'exam'),
(3, 1, 2, '2023-04-01', 'C', 90, 85, 'exam'),
(4, 2, 2, '2023-04-01', 'C', 90, 85, 'exam');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `profile_picture` varchar(255) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `school` varchar(100) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `grade` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `speciality` varchar(50) DEFAULT NULL,
  `level` varchar(20) DEFAULT NULL,
  `password` varchar(99) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `name`, `profile_picture`, `phone_number`, `school`, `age`, `grade`, `email`, `speciality`, `level`, `password`) VALUES
(1, 'John Smith', 'https://example.com/profiles/john.jpg', '555-1234', 'ABC High School', 16, '10th', 'john.smith@example.com', 'Mathematics', 'Secondary', '123456'),
(2, 'Jane Doe', 'https://example.com/profiles/jane.jpg', '555-5678', 'XYZ High School', 17, '11th', 'jane.doe@example.com', 'English Literature', 'Secondary', '123456'),
(3, 'John Doe', NULL, NULL, NULL, 18, '12th', 'johndoe@example.com', NULL, 'high school', ''),
(6, 'John Doe', NULL, '555-1234', 'Example School', 18, '12', 'johnd4oe@example.com', 'Mathematics', NULL, 'password123'),
(7, 'John Doe', NULL, '555-1234', 'Example School', 18, '12', 'johnd44oe@example.com', 'Mathematics', NULL, ''),
(8, 'John Doe', NULL, '555-1234', 'Example School', 18, '12', 'johnd4ss4oe@example.com', 'Mathematics', NULL, 'ss55555555'),
(9, 'John Doe', NULL, '555-1234', 'Example School', 18, '12', 'zcool@example.com', 'Mathematics', NULL, '12021995'),
(10, 'John Doe', NULL, '555-1234', 'Example School', 18, '12', 'zcool2@example.com', 'Mathematics', NULL, '12021995'),
(11, 'John Doe', NULL, '555-1234', 'Example School', 18, '12', 'zcool3@example.com', 'Mathematics', NULL, '12021995'),
(12, 'John Doe', NULL, '555-1234', 'Example School', 18, '12', 'zcool4@example.com', 'Mathematics', NULL, '12021995'),
(13, 'John Doe', NULL, '555-1234', 'Example School', 18, '12', 'zcool5@example.com', 'Mathematics', NULL, '12021995');

-- --------------------------------------------------------

--
-- Table structure for table `student_classes`
--

CREATE TABLE `student_classes` (
  `student_id` int(11) NOT NULL,
  `class_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `student_classes`
--

INSERT INTO `student_classes` (`student_id`, `class_id`) VALUES
(1, 1),
(1, 2),
(2, 2);

-- --------------------------------------------------------

--
-- Table structure for table `teachers`
--

CREATE TABLE `teachers` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `profile_picture` varchar(255) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `school` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `article` varchar(255) DEFAULT NULL,
  `grades` varchar(255) DEFAULT NULL,
  `level` varchar(20) DEFAULT NULL,
  `password` varchar(99) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `teachers`
--

INSERT INTO `teachers` (`id`, `name`, `profile_picture`, `phone_number`, `school`, `email`, `location`, `article`, `grades`, `level`, `password`) VALUES
(1, 'James Johnson', 'https://example.com/profiles/james.jpg', '555-4321', 'DEF University', 'james.johnson@example.com', 'New York, NY', 'Introduction to Calculus', '9-12', 'Secondary', '12345678'),
(2, 'Emily Davis', 'https://example.com/profiles/emily.jpg', '555-8765', 'GHI College', 'emily.davis@example.com', 'San Francisco, CA', 'Creative Writing', '9-12', 'Secondary', '12345678'),
(3, 'Jane Smith', NULL, NULL, NULL, 'janesmith@example.com', 'New York', NULL, '9th-12th', 'high school', ''),
(4, 'Jane Doe', 'https://example.com/profile.jpg', '1234567890', 'Example School', 'janedoe@example.com', 'New York, NY', 'Example article', '1-5', 'Elementary', ''),
(8, 'Jane Doe', 'https://example.com/profile.jpg', '1234567890', 'Example School', 'janedoe2@example.com', 'New York, NY', 'Example article', '1-5', 'Elementary', ''),
(9, 'Jane Doe', 'https://example.com/profile.jpg', '1234567890', 'Example School', 'janedoe3@example.com', 'New York, NY', 'Example article', '1-5', 'Elementary', ''),
(10, 'Jane Doe', 'https://example.com/profile.jpg', '1234567890', 'Example School', 'janedoe4@example.com', 'New York, NY', 'Example article', '1-5', 'Elementary', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `classes`
--
ALTER TABLE `classes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `teacher_id` (`teacher_id`);

--
-- Indexes for table `enrollment`
--
ALTER TABLE `enrollment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `class_id` (`class_id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `student_classes`
--
ALTER TABLE `student_classes`
  ADD PRIMARY KEY (`student_id`,`class_id`),
  ADD KEY `class_id` (`class_id`);

--
-- Indexes for table `teachers`
--
ALTER TABLE `teachers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(22) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `admins`
--
ALTER TABLE `admins`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `classes`
--
ALTER TABLE `classes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `enrollment`
--
ALTER TABLE `enrollment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `teachers`
--
ALTER TABLE `teachers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `classes`
--
ALTER TABLE `classes`
  ADD CONSTRAINT `classes_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`id`);

--
-- Constraints for table `enrollment`
--
ALTER TABLE `enrollment`
  ADD CONSTRAINT `enrollment_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`),
  ADD CONSTRAINT `enrollment_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`);

--
-- Constraints for table `student_classes`
--
ALTER TABLE `student_classes`
  ADD CONSTRAINT `student_classes_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`),
  ADD CONSTRAINT `student_classes_ibfk_2` FOREIGN KEY (`class_id`) REFERENCES `classes` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
