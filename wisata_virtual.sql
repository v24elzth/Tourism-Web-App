-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3307
-- Generation Time: May 15, 2026 at 05:26 AM
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
-- Database: `wisata_virtual`
--

-- --------------------------------------------------------

--
-- Table structure for table `lokasi`
--

CREATE TABLE `lokasi` (
  `id` int(11) NOT NULL,
  `nama_lokasi` varchar(100) NOT NULL,
  `gambar` varchar(255) NOT NULL DEFAULT 'default_lokasi.jpg',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `lokasi`
--

INSERT INTO `lokasi` (`id`, `nama_lokasi`, `gambar`, `created_at`, `updated_at`) VALUES
(1, 'West Nusa Tenggara', 'NTB.jpg', '2026-05-01 03:19:49', '2026-05-01 03:19:49'),
(2, 'South Sulawesi', 'SULSEL.jpg', '2026-05-01 03:26:24', '2026-05-01 03:26:24'),
(3, 'North Sumatera', 'SUMUT.jpg', '2026-05-01 03:28:07', '2026-05-01 03:28:07'),
(4, 'Bali', 'BALI.jpg', '2026-05-01 03:29:09', '2026-05-01 05:19:04'),
(6, 'East Java', 'JATIM.jpg', '2026-05-01 04:47:25', '2026-05-01 04:47:25'),
(8, 'West Java', 'JABAR.jpg', '2026-05-01 05:21:40', '2026-05-01 05:21:40'),
(9, 'Central Java', 'JATENG.jpg', '2026-05-01 05:22:04', '2026-05-01 05:22:04');

-- --------------------------------------------------------

--
-- Table structure for table `pemesanan`
--

CREATE TABLE `pemesanan` (
  `id` int(11) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `total_harga` decimal(15,2) DEFAULT NULL,
  `status` varchar(10) DEFAULT 'Pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `pemesanan_detail`
--

CREATE TABLE `pemesanan_detail` (
  `id` int(11) NOT NULL,
  `id_pemesanan` int(11) DEFAULT NULL,
  `id_wisata` int(11) DEFAULT NULL,
  `qty` int(11) DEFAULT NULL,
  `subtotal` decimal(15,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','user') DEFAULT 'user',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `nama`, `email`, `password`, `role`, `created_at`, `updated_at`) VALUES
(13, 'Admin1', 'admin1@example.com', '$2b$12$Q1nOKNTYTQLHkuzmybyEqOzEOXEgHBJF./5OFJh9/6SNg8ExmPj22', 'admin', '2026-05-09 05:57:30', '2026-05-09 05:57:30'),
(14, 'User1', 'user1@example.com', '$2b$12$ke2ZSE.pbuPSopRcv5s5KukahnH/lkgDEVOOlNxIx0m5NGwjhh1Bq', 'user', '2026-05-09 05:57:54', '2026-05-09 05:57:54');

-- --------------------------------------------------------

--
-- Table structure for table `wisata`
--

CREATE TABLE `wisata` (
  `id` int(11) NOT NULL,
  `id_lokasi` int(11) NOT NULL,
  `gambar` varchar(255) NOT NULL DEFAULT 'default_wisata.jpg',
  `nama_wisata` varchar(100) NOT NULL,
  `harga` int(11) NOT NULL,
  `durasi` int(11) NOT NULL,
  `deskripsi` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`deskripsi`)),
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `wisata`
--

INSERT INTO `wisata` (`id`, `id_lokasi`, `gambar`, `nama_wisata`, `harga`, `durasi`, `deskripsi`, `created_at`, `updated_at`) VALUES
(9, 4, 'bali_p3_beach.jpg', 'Denpasar City & Coastal Escape', 2720000, 3, '{\"Day 1\": [\"Pantai Sanur\", \"Monumen Bajra Sandhi\", \"Museum Bali\", \"Lunch:  Nasi Ayam Kedewatan\", \"Tukad Badung Riverside Walk\", \"Dinner: Cafe Tukad Badung\"], \"Day 2\": [\"Big Garden Corner\", \"Mangrove Suwung\", \"Lunch: Bebek Bengil\", \"Dinner: Seafood Sanur\"], \"Day 3\": [\"Beli oleh-oleh \", \"Makan Kuliner Bali\"]}', '2026-05-08 09:28:49', '2026-05-08 09:28:49'),
(10, 4, 'bali_p2_monyet.jpg', 'Ubud Culture & Nature Immersion', 4325000, 4, '{\"Day 1\": [\"check-in vila\", \"Monkey Forest Ubud\", \"Dinner: Locavore To Go\"], \"Day 2\": [\"Tegalalang Rice Terrace\", \"Tirta Empul\", \"Lunch: Warung lokal Ubud\", \"Kopi luwak tasting\"], \"Day 3\": [\"Air Terjun Tegenungan\", \"Jelajah alam sekitar Ubud\", \"Lunch and Dinner: Villa\"], \"Day 4\": [\"Belanja oleh-oleh khas Ubud\", \"Check-out vila\"]}', '2026-05-08 09:34:49', '2026-05-08 09:57:24'),
(11, 9, 'yogya_p1_city.jpg', 'Yogyakarta City Heritage', 1420000, 3, '{\"Day 1\": [\"check-in hotel\", \"Keraton Yogyakarta\", \"Taman Sari Water Castle\", \"Dinner: Gudeg Yu Djum\", \"Jalan malam Malioboro\"], \"Day 2\": [\"Eksplor Malioboro\", \"Museum Sonobudoyo\", \"Lunch:  Sate Klathak P.Pong\", \"Wisata kuliner\"], \"Day 3\": [\"Beli oleh-oleh\", \"Beli oleh-oleh\"]}', '2026-05-08 09:56:28', '2026-05-08 09:56:28'),
(12, 9, 'yogya01.jpg', 'Yogyakarta Grand Explorer', 2775000, 4, '{\"Day 1\": [\"check-in hotel kota\", \"Eksplor Malioboro\", \"Dinner: Gudeg Yu Djum\"], \"Day 2\": [\"Candi Borobudur\", \"Wisata Kuliner \"], \"Day 3\": [\"Candi Prambanan\", \"Cave tubing di Goa Pindul\", \"Lunch: Sate Klathak Pak Pong\"], \"Day 4\": [\"Belanja oleh-oleh\", \"Check-out\"]}', '2026-05-08 10:10:55', '2026-05-08 10:10:55'),
(13, 9, 'semarang02.jpg', 'Semarang Heritage & Culinary', 1135000, 2, '{\"Day 1\": [\"Check-in hotel\", \"Lawang Sewu\", \"Kota Lama Semarang\", \"Eat Bandeng Presto\"], \"Day 2\": [\"Sam Poo Kong\", \"Wisata Kuliner\", \"Beli oleh-oleh\", \"Check-out\"]}', '2026-05-08 10:13:30', '2026-05-08 10:13:30'),
(14, 9, 'borobudur.jpg', 'Borobudur & Magelang Nature Escape', 2525000, 3, '{\"Day 1\": [\"Check-in\", \"Candi Borobudur\", \"Lunch: Kupat Tahu Pojok\", \"Sunset di Punthuk Setumbu\", \"Dinner: Wedang Kacang\"], \"Day 2\": [\"Sunrise di Punthuk Setumbu\", \"Curug Silawe\", \"Wisata Kuliner\"], \"Day 3\": [\"Belanja oleh-oleh\", \"Check-out\"]}', '2026-05-08 10:18:32', '2026-05-08 10:18:32'),
(15, 6, 'surabaya01.jpg', 'Surabaya City & Heritage Tour', 1300000, 3, '{\"Day 1\": [\"Check-in\", \"House of Sampoerna\", \"Lunch: Rawon Setan\", \"Monumen Kapal Selam\", \"Dinner: Rujak Cingur\"], \"Day 2\": [\"Surabaya North Quay\", \"Eksplor Jembatan Merah\", \"Kuliner khas Surabaya\", \"Belanja di Pasar Atom\"], \"Day 3\": [\"Museum 10 November\", \"Belanja oleh-oleh\", \"Chack-out\"]}', '2026-05-08 10:23:01', '2026-05-08 10:23:01'),
(16, 6, 'malang05.jpg', 'Malang & Batu Nature Adventure', 3790000, 4, '{\"Day 1\": [\"Tiba di Malang\", \"Eksplor kota Malang\", \"Dinner: Bakso President\"], \"Day 2\": [\"Museum Angkut\", \"Lunch: Kuliner lokal Batu\", \"Taman Selecta\", \"Dinner: Kuliner Batu\"], \"Day 3\": [\"Jatim Park 1\", \"Eksplor alun-alun Batu\"], \"Day 4\": [\"Air Terjun Malang\", \"Belanja oleh-oleh\", \"Check-out\"]}', '2026-05-08 10:26:43', '2026-05-08 10:26:43'),
(17, 8, 'jabar_bandung_p1.png', 'Bandung City & Culinary Escape', 1180000, 2, '{\"Day 1\": [\"Gedung Sate\", \"Jalan Braga\", \"Lunch: Batagor Kingsley\"], \"Day 2\": [\"Floating Market\", \"Tangkuban Perahu\"]}', '2026-05-08 10:40:10', '2026-05-08 10:40:10'),
(18, 8, 'jabar_bogor_p2.png', 'Exploring Taman Safari', 2325000, 2, '{\"Day 1\": [\"Kebun Raya Bogor\", \"Lunch: Soto Bogor\"], \"Day 2\": [\"Taman Safari\"]}', '2026-05-08 11:21:39', '2026-05-08 11:21:39'),
(20, 3, 'sumut_medan_p1.png', 'Medan City & Berastagi Heritage', 3980000, 4, '{\"Day 1\": [\"Istana Maimun\", \"Kesawan\", \"Tjong A Fie\"], \"Day 2\": [\"Breakfast: Lontong Kak Lin\", \"Bukit Gundaling\", \"Dinner: Naniura\"], \"Day 3\": [\"Air Terjun Sipiso-piso\", \"Parapat/TukTuk\", \"Sunset di Danau Toba\"], \"Day 4\": [\"Pulau Samosir\", \"Batu Gantung\", \"Makam Raja Sidabutar\"]}', '2026-05-08 11:27:51', '2026-05-08 11:27:51'),
(21, 2, 'sulsel_p1.jpg', 'Toraja Culture & Nature Escape', 4590000, 2, '{\"Day 1\": [\"Desa adat Kete Kesu\", \"Lunch: Pa\'piong\", \"Situs makam Tebing Lemo\", \"Kopi Toraja\"], \"Day 2\": [\"Batu Tumonga\", \"Gereja Batu\"]}', '2026-05-08 11:34:43', '2026-05-08 11:34:43'),
(22, 2, 'sulsel_p2.jpg', 'Makassar Heritage', 3375000, 3, '{\"Day 1\": [\"Pantai Losari\", \"Benteng Rotterdam\", \"Lunch: Coto Makassar\"], \"Day 2\": [\"Pulau Samalona\", \"Lunch: Sop Konro\"], \"Day 3\": [\"Rammang-rammang\", \"Oleh-oleh hunting\"]}', '2026-05-08 11:36:08', '2026-05-08 11:36:08'),
(23, 1, 'ntb_lombok_p2.jpg', 'Lombok Mainland', 3515000, 4, '{\"Day 1\": [\"Sengigi Beach\", \"Lunch: Nasi Balap Puyung\", \"Dinner: Sate Rembiga\"], \"Day 2\": [\"Sirkuit Mandalika\", \"Bukit Merese\", \"Desa Adat Sasak\"], \"Day 3\": [\"Explore 3\'s Gili\", \"Seafood at Gili Trawangan\"], \"Day 4\": [\"Pink Beach\", \"Pantai Kuta\"]}', '2026-05-08 11:38:30', '2026-05-08 11:44:38');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `lokasi`
--
ALTER TABLE `lokasi`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pemesanan`
--
ALTER TABLE `pemesanan`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_user` (`id_user`);

--
-- Indexes for table `pemesanan_detail`
--
ALTER TABLE `pemesanan_detail`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_pemesanan` (`id_pemesanan`),
  ADD KEY `id_wisata` (`id_wisata`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `wisata`
--
ALTER TABLE `wisata`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_lokasi` (`id_lokasi`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `lokasi`
--
ALTER TABLE `lokasi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `pemesanan`
--
ALTER TABLE `pemesanan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `pemesanan_detail`
--
ALTER TABLE `pemesanan_detail`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `wisata`
--
ALTER TABLE `wisata`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `pemesanan`
--
ALTER TABLE `pemesanan`
  ADD CONSTRAINT `pemesanan_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `pemesanan_detail`
--
ALTER TABLE `pemesanan_detail`
  ADD CONSTRAINT `pemesanan_detail_ibfk_1` FOREIGN KEY (`id_pemesanan`) REFERENCES `pemesanan` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `pemesanan_detail_ibfk_2` FOREIGN KEY (`id_wisata`) REFERENCES `wisata` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `wisata`
--
ALTER TABLE `wisata`
  ADD CONSTRAINT `wisata_ibfk_1` FOREIGN KEY (`id_lokasi`) REFERENCES `lokasi` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
