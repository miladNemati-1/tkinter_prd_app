-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Oct 14, 2022 at 03:46 AM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Chemistry`
--

-- --------------------------------------------------------

--
-- Table structure for table `account_emailaddress`
--

CREATE TABLE `account_emailaddress` (
  `id` int(11) NOT NULL,
  `verified` longtext CHARACTER SET utf8 NOT NULL,
  `primary` longtext CHARACTER SET utf8 NOT NULL,
  `user_id` longtext CHARACTER SET utf8 NOT NULL,
  `email` varchar(254) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `account_emailaddress`
--

INSERT INTO `account_emailaddress` (`id`, `verified`, `primary`, `user_id`, `email`) VALUES
(1, '1', '1', '1', 'mnem0001@student.monash.edu'),
(2, '0', '1', '2', 'arshiaadouli@gmail.com'),
(3, '0', '1', '3', 'aado0001@student.monash.edu');

-- --------------------------------------------------------

--
-- Table structure for table `account_emailconfirmation`
--

CREATE TABLE `account_emailconfirmation` (
  `id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `sent` datetime DEFAULT NULL,
  `key` varchar(64) CHARACTER SET utf8 NOT NULL,
  `email_address_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8 NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `content_type_id`, `codename`, `name`) VALUES
(1, 1, 'add_logentry', 'Can add log entry'),
(2, 1, 'change_logentry', 'Can change log entry'),
(3, 1, 'delete_logentry', 'Can delete log entry'),
(4, 1, 'view_logentry', 'Can view log entry'),
(5, 2, 'add_permission', 'Can add permission'),
(6, 2, 'change_permission', 'Can change permission'),
(7, 2, 'delete_permission', 'Can delete permission'),
(8, 2, 'view_permission', 'Can view permission'),
(9, 3, 'add_group', 'Can add group'),
(10, 3, 'change_group', 'Can change group'),
(11, 3, 'delete_group', 'Can delete group'),
(12, 3, 'view_group', 'Can view group'),
(13, 4, 'add_contenttype', 'Can add content type'),
(14, 4, 'change_contenttype', 'Can change content type'),
(15, 4, 'delete_contenttype', 'Can delete content type'),
(16, 4, 'view_contenttype', 'Can view content type'),
(17, 5, 'add_session', 'Can add session'),
(18, 5, 'change_session', 'Can change session'),
(19, 5, 'delete_session', 'Can delete session'),
(20, 5, 'view_session', 'Can view session'),
(21, 6, 'add_site', 'Can add site'),
(22, 6, 'change_site', 'Can change site'),
(23, 6, 'delete_site', 'Can delete site'),
(24, 6, 'view_site', 'Can view site'),
(25, 7, 'add_emailaddress', 'Can add email address'),
(26, 7, 'change_emailaddress', 'Can change email address'),
(27, 7, 'delete_emailaddress', 'Can delete email address'),
(28, 7, 'view_emailaddress', 'Can view email address'),
(29, 8, 'add_emailconfirmation', 'Can add email confirmation'),
(30, 8, 'change_emailconfirmation', 'Can change email confirmation'),
(31, 8, 'delete_emailconfirmation', 'Can delete email confirmation'),
(32, 8, 'view_emailconfirmation', 'Can view email confirmation'),
(33, 9, 'add_socialaccount', 'Can add social account'),
(34, 9, 'change_socialaccount', 'Can change social account'),
(35, 9, 'delete_socialaccount', 'Can delete social account'),
(36, 9, 'view_socialaccount', 'Can view social account'),
(37, 10, 'add_socialapp', 'Can add social application'),
(38, 10, 'change_socialapp', 'Can change social application'),
(39, 10, 'delete_socialapp', 'Can delete social application'),
(40, 10, 'view_socialapp', 'Can view social application'),
(41, 11, 'add_socialtoken', 'Can add social application token'),
(42, 11, 'change_socialtoken', 'Can change social application token'),
(43, 11, 'delete_socialtoken', 'Can delete social application token'),
(44, 11, 'view_socialtoken', 'Can view social application token'),
(45, 12, 'add_user', 'Can add user'),
(46, 12, 'change_user', 'Can change user'),
(47, 12, 'delete_user', 'Can delete user'),
(48, 12, 'view_user', 'Can view user'),
(49, 13, 'add_country', 'Can add Country'),
(50, 13, 'change_country', 'Can change Country');

-- --------------------------------------------------------

--
-- Table structure for table `chemicals_cas`
--

CREATE TABLE `chemicals_cas` (
  `id` int(11) NOT NULL,
  `cas` varchar(31) CHARACTER SET utf8 NOT NULL,
  `inchi_id` longtext CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `chemicals_cas`
--

INSERT INTO `chemicals_cas` (`id`, `cas`, `inchi_id`) VALUES
(1, '141-78-6', '1');

-- --------------------------------------------------------

--
-- Table structure for table `chemicals_inchi`
--

CREATE TABLE `chemicals_inchi` (
  `id` int(11) NOT NULL,
  `inchi` varchar(511) CHARACTER SET utf8 NOT NULL,
  `inchi_key` varchar(27) CHARACTER SET utf8 NOT NULL,
  `mw` longtext CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `chemicals_inchi`
--

INSERT INTO `chemicals_inchi` (`id`, `inchi`, `inchi_key`, `mw`) VALUES
(1, '1S/C4H8O2/c1-3-6-4(2)5/h3H2,1-2H3', 'XEKOWRVHYACXOJ-UHFFFAOYSA-N', '88.106'),
(2, 'asd', 'sad', '111');

-- --------------------------------------------------------

--
-- Table structure for table `chemicals_name`
--

CREATE TABLE `chemicals_name` (
  `id` int(11) NOT NULL,
  `name` varchar(511) CHARACTER SET utf8 NOT NULL,
  `iupac` longtext CHARACTER SET utf8 NOT NULL,
  `common_name` longtext CHARACTER SET utf8 NOT NULL,
  `abbreviation` longtext CHARACTER SET utf8 NOT NULL,
  `inchi_id` longtext CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `chemicals_name`
--

INSERT INTO `chemicals_name` (`id`, `name`, `iupac`, `common_name`, `abbreviation`, `inchi_id`) VALUES
(1, 'Ethyl acetate', '1', '1', '0', '1'),
(2, 'EA', '0', '0', '1', '1'),
(3, 'Ethyl acetate', '0', '0', '0', '1'),
(4, 'Acetic acid ethyl ester', '0', '0', '0', '1'),
(5, 'Ethyl ethanoate', '0', '0', '0', '1'),
(6, '141-78-6', '0', '0', '0', '1'),
(7, 'HSDB 83', '0', '0', '0', '1'),
(8, 'NSC 70930', '0', '0', '0', '1'),
(9, 'Octan etylu [Polish]', '0', '0', '0', '1'),
(10, 'RCRA waste no. U112', '0', '0', '0', '1'),
(11, 'RCRA waste number U112', '0', '0', '0', '1'),
(12, 'UN1173', '0', '0', '0', '1'),
(13, '676810_SIAL', '0', '0', '0', '1'),
(14, 'ST5214347', '0', '0', '0', '1'),
(15, '1-acetoxyethane', '0', '0', '0', '1'),
(16, '45767_FLUKA', '0', '0', '0', '1'),
(17, 'NCGC00091766-01', '0', '0', '0', '1'),
(18, 'sadasd', '1', '0', '0', '2'),
(19, 'asdasd', '0', '1', '0', '2'),
(20, 'asd', '0', '0', '1', '2');

-- --------------------------------------------------------

--
-- Table structure for table `chemicals_smiles`
--

CREATE TABLE `chemicals_smiles` (
  `id` int(11) NOT NULL,
  `smiles` varchar(511) CHARACTER SET utf8 NOT NULL,
  `inchi_id` longtext CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `chemicals_smiles`
--

INSERT INTO `chemicals_smiles` (`id`, `smiles`, `inchi_id`) VALUES
(1, 'CCOC(C)=O', '1');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `object_id` longtext CHARACTER SET utf8 DEFAULT NULL,
  `object_repr` varchar(200) CHARACTER SET utf8 NOT NULL,
  `action_flag` longtext CHARACTER SET utf8 NOT NULL,
  `change_message` longtext CHARACTER SET utf8 NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` longtext CHARACTER SET utf8 NOT NULL,
  `action_time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`, `action_time`) VALUES
(1, '1', 'N/A', '1', '[{\"added\": {}}]', 21, '1', '2022-08-23 06:42:47'),
(2, '2', 'Sigma-Aldrich', '1', '[{\"added\": {}}]', 21, '1', '2022-08-23 06:42:57'),
(3, '1', 'Ethyl acetate', '2', '[{\"changed\": {\"fields\": [\"Common name\"]}}]', 19, '1', '2022-08-23 06:43:39');

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) CHARACTER SET utf8 NOT NULL,
  `model` varchar(100) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(7, 'account', 'emailaddress'),
(8, 'account', 'emailconfirmation'),
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(20, 'chemicals', 'cas'),
(17, 'chemicals', 'inchi'),
(19, 'chemicals', 'name'),
(18, 'chemicals', 'smiles'),
(4, 'contenttypes', 'contenttype'),
(21, 'experiments', 'company'),
(22, 'experiments', 'experiment'),
(23, 'experiments', 'experiment_chemicals'),
(24, 'experiments', 'inventory'),
(25, 'experiments', 'reactor'),
(28, 'measurements', 'data'),
(26, 'measurements', 'device'),
(27, 'measurements', 'measurement'),
(5, 'sessions', 'session'),
(6, 'sites', 'site'),
(9, 'socialaccount', 'socialaccount'),
(10, 'socialaccount', 'socialapp'),
(11, 'socialaccount', 'socialtoken'),
(13, 'users', 'country'),
(14, 'users', 'group'),
(16, 'users', 'institution'),
(12, 'users', 'user'),
(15, 'users', 'user_group');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) CHARACTER SET utf8 NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 NOT NULL,
  `applied` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2022-08-23 06:26:28'),
(2, 'contenttypes', '0002_remove_content_type_name', '2022-08-23 06:26:28'),
(3, 'auth', '0001_initial', '2022-08-23 06:26:28'),
(4, 'auth', '0002_alter_permission_name_max_length', '2022-08-23 06:26:28'),
(5, 'auth', '0003_alter_user_email_max_length', '2022-08-23 06:26:28'),
(6, 'auth', '0004_alter_user_username_opts', '2022-08-23 06:26:28'),
(7, 'auth', '0005_alter_user_last_login_null', '2022-08-23 06:26:28'),
(8, 'auth', '0006_require_contenttypes_0002', '2022-08-23 06:26:28'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2022-08-23 06:26:28'),
(10, 'auth', '0008_alter_user_username_max_length', '2022-08-23 06:26:28'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2022-08-23 06:26:28'),
(12, 'auth', '0010_alter_group_name_max_length', '2022-08-23 06:26:28'),
(13, 'auth', '0011_update_proxy_permissions', '2022-08-23 06:26:28'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2022-08-23 06:26:28'),
(15, 'users', '0001_initial', '2022-08-23 06:26:29'),
(16, 'account', '0001_initial', '2022-08-23 06:26:29'),
(17, 'account', '0002_email_max_length', '2022-08-23 06:26:29'),
(18, 'admin', '0001_initial', '2022-08-23 06:26:29'),
(19, 'admin', '0002_logentry_remove_auto_add', '2022-08-23 06:26:29'),
(20, 'admin', '0003_logentry_add_action_flag_choices', '2022-08-23 06:26:29'),
(21, 'chemicals', '0001_initial', '2022-08-23 06:26:29'),
(22, 'experiments', '0001_initial', '2022-08-23 06:26:29'),
(23, 'experiments', '0002_initial', '2022-08-23 06:26:29'),
(24, 'experiments', '0003_alter_inventory_purity', '2022-08-23 06:26:29'),
(25, 'experiments', '0004_alter_inventory_purity', '2022-08-23 06:26:29'),
(26, 'experiments', '0005_alter_inventory_inchi', '2022-08-23 06:26:29'),
(27, 'measurements', '0001_initial', '2022-08-23 06:26:29'),
(28, 'sessions', '0001_initial', '2022-08-23 06:26:29'),
(29, 'sites', '0001_initial', '2022-08-23 06:26:29'),
(30, 'sites', '0002_alter_domain_unique', '2022-08-23 06:26:29'),
(31, 'socialaccount', '0001_initial', '2022-08-23 06:26:29'),
(32, 'socialaccount', '0002_token_max_lengths', '2022-08-23 06:26:29'),
(33, 'socialaccount', '0003_extra_data_default_dict', '2022-08-23 06:26:29');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) CHARACTER SET utf8 NOT NULL,
  `session_data` longtext CHARACTER SET utf8 NOT NULL,
  `expire_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('6l63m3ukz2bysztkkc2gykd5ne9vcb8z', '.eJxVjEEOwiAQAP_C2RAoW6Q9evcNZBe2FjVgoE00xr-bJr30OjOZr_CNW0sle36_Uv2IUZ2Ex3WZ_dq4-hTFKLQ4MMLw4LyJeMd8KzKUvNREckvkbpu8lsjPy94eBjO2eduqHuLk3HkgtFZ3GCDyYPVkAwU3ABjqkUBbY4AnRtZkQFnTheAMqU78_ggZPwA:1oQNPz:mQZINznit_cLlzu1wSFa7ik-djMuy2z1GEnYEXMrYIE', '2022-09-06 06:29:43'),
('jg2a7qc6j9delckk8vczfdtwjtl76eyw', '.eJxVjEEOwiAQAP_C2RAoW6Q9evcNZBe2FjVgSptojH83JD3odWYyb-FxW2e_VV58imIUWhx-GWG4cW4iXjFfigwlr0si2RK52yrPJfL9tLd_gxnr3Laqhzg5dxwIrdUdBog8WD3ZQMENAIZ6JNDWGOCJkTUZUNZ0IThDqmvTyrWmkj0_H2l5iVF9voTAPwA:1oiCgS:6pkU2ydr56ACqh5uhhhy5v4DdbPdvzF3v3nWGxE-ALE', '2022-10-25 10:40:24'),
('vafriosao0mergeou4d1dgem9d7ns04b', 'eyJhY2NvdW50X3ZlcmlmaWVkX2VtYWlsIjpudWxsLCJhY2NvdW50X3VzZXIiOiIzIn0:1oRXNI:WAI4pagZ1pXkoe_2vBsuOG1nqaR55zx--u9q7efufw8', '2022-09-09 11:19:44');

-- --------------------------------------------------------

--
-- Table structure for table `django_site`
--

CREATE TABLE `django_site` (
  `id` int(11) NOT NULL,
  `name` varchar(50) CHARACTER SET utf8 NOT NULL,
  `domain` varchar(100) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_site`
--

INSERT INTO `django_site` (`id`, `name`, `domain`) VALUES
(1, 'example.com', 'example.com');

-- --------------------------------------------------------

--
-- Table structure for table `experiments_company`
--

CREATE TABLE `experiments_company` (
  `id` int(11) NOT NULL,
  `name` varchar(60) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `experiments_company`
--

INSERT INTO `experiments_company` (`id`, `name`) VALUES
(1, 'N/A'),
(2, 'Sigma-Aldrich');

-- --------------------------------------------------------

--
-- Table structure for table `experiments_experiment`
--

CREATE TABLE `experiments_experiment` (
  `id` int(11) NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `name` varchar(127) CHARACTER SET utf8 NOT NULL,
  `temperature` longtext CHARACTER SET utf8 NOT NULL,
  `total_volume` longtext CHARACTER SET utf8 NOT NULL,
  `reactor_id` longtext CHARACTER SET utf8 DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `experiments_experiment`
--

INSERT INTO `experiments_experiment` (`id`, `date`, `time`, `name`, `temperature`, `total_volume`, `reactor_id`, `user_id`) VALUES
(73, '2022-10-13', '16:08:03', 'experiment_1', '12', '32', NULL, 1),
(74, '2022-10-13', '16:09:04', 'experiment_2', '25', '35', NULL, 1),
(75, '2022-10-13', '16:11:27', 'experiment_3', '45', '54', NULL, 2),
(76, '2022-10-13', '16:11:41', 'experiment_6', '43', '23', NULL, 1),
(77, '2022-10-13', '16:33:27', 'experiment_7', '12', '32', NULL, 2),
(78, '2022-10-13', '16:36:08', 'experiment_8', '67', '34', NULL, 2),
(79, '2022-10-13', '16:38:36', 'experiment_9', '23', '32', NULL, 2),
(80, '2022-10-13', '16:39:34', 'experiment_10', '32', '32', NULL, 1),
(81, '2022-10-13', '16:40:25', 'experiment_11', '23', '43', NULL, 2),
(82, '2022-10-13', '16:41:01', 'experiment_12', '34', '78', NULL, 1),
(83, '2022-10-13', '16:41:49', 'experiment_13', '13', '13', NULL, 1),
(84, '2022-10-13', '16:43:09', 'experiment_14', '45', '54', NULL, 1),
(85, '2022-10-13', '16:44:02', 'experiment_14', '14', '14', NULL, 1),
(86, '2022-10-13', '16:48:11', 'experiment_16', '16', '16', NULL, 1),
(87, '2022-10-13', '16:49:23', 'experiment_17', '17', '17', NULL, 1),
(88, '2022-10-13', '21:11:19', 'exp_a_1', '23', '32', NULL, 2),
(89, '2022-10-13', '21:12:05', 'ex_b_1', '23', '12', NULL, 3),
(90, '2022-10-13', '21:15:21', 'exp_one_test', '20', '32', NULL, 1);

-- --------------------------------------------------------

--
-- Table structure for table `experiments_experiment_chemicals`
--

CREATE TABLE `experiments_experiment_chemicals` (
  `id` int(11) NOT NULL,
  `type` varchar(1) CHARACTER SET utf8 NOT NULL,
  `molarity` longtext CHARACTER SET utf8 NOT NULL,
  `experiment_id` longtext CHARACTER SET utf8 NOT NULL,
  `inventory_id` longtext CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `experiments_experiment_chemicals`
--

INSERT INTO `experiments_experiment_chemicals` (`id`, `type`, `molarity`, `experiment_id`, `inventory_id`) VALUES
(1, 'M', '4', '1', '1'),
(2, 'I', '1', '2', '1');

-- --------------------------------------------------------

--
-- Table structure for table `experiments_inventory`
--

CREATE TABLE `experiments_inventory` (
  `id` int(11) NOT NULL,
  `extra_info` varchar(511) CHARACTER SET utf8 NOT NULL,
  `url` varchar(511) CHARACTER SET utf8 NOT NULL,
  `company_id` longtext CHARACTER SET utf8 NOT NULL,
  `group_id` longtext CHARACTER SET utf8 NOT NULL,
  `inchi_id` longtext CHARACTER SET utf8 NOT NULL,
  `purity` longtext CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `experiments_inventory`
--

INSERT INTO `experiments_inventory` (`id`, `extra_info`, `url`, `company_id`, `group_id`, `inchi_id`, `purity`) VALUES
(1, '', '', '1', '1', '1', '99');

-- --------------------------------------------------------

--
-- Table structure for table `experiments_reactor`
--

CREATE TABLE `experiments_reactor` (
  `id` int(11) NOT NULL,
  `name` varchar(30) CHARACTER SET utf8 NOT NULL,
  `volume` longtext CHARACTER SET utf8 NOT NULL,
  `type` varchar(1) CHARACTER SET utf8 NOT NULL,
  `group_id` longtext CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `measurements_data`
--

CREATE TABLE `measurements_data` (
  `id` int(11) NOT NULL,
  `res_time` longtext CHARACTER SET utf8 NOT NULL,
  `result` longtext CHARACTER SET utf8 NOT NULL,
  `measurement_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `measurements_data`
--

INSERT INTO `measurements_data` (`id`, `res_time`, `result`, `measurement_id`) VALUES
(2522, '60', '6969', 49),
(2523, '120', '6969', 49),
(2524, '180', '6969', 49),
(2525, '240', '6969', 49),
(2526, '300', '6969', 49),
(2527, '360', '6969', 49),
(2528, '420', '6969', 49),
(2529, '480', '6969', 49),
(2530, '540', '6969', 49),
(2531, '600', '6969', 49),
(2532, '660', '6969', 49),
(2533, '720', '6969', 49),
(2534, '780', '6969', 49),
(2535, '840', '6969', 49),
(2536, '900', '6969', 49),
(2537, '960', '6969', 49),
(2538, '1020', '6969', 49),
(2539, '1080', '6969', 49),
(2540, '1140', '6969', 49),
(2541, '1200', '6969', 49),
(2542, '1260', '6969', 49),
(2543, '1320', '6969', 49),
(2544, '1380', '6969', 49),
(2545, '1440', '6969', 49),
(2546, '1500', '6969', 49),
(2547, '1560', '6969', 49),
(2548, '1620', '6969', 49),
(2549, '1680', '6969', 49),
(2550, '1740', '6969', 49),
(2551, '1800', '6969', 49),
(2552, '1860', '6969', 49),
(2553, '1920', '6969', 49),
(2554, '1980', '6969', 49),
(2555, '2040', '6969', 49),
(2556, '2100', '6969', 49),
(2557, '2160', '6969', 49),
(2558, '2220', '6969', 49),
(2559, '2280', '6969', 49),
(2560, '2340', '6969', 49),
(2561, '2400', '6969', 49),
(2562, '2460', '6969', 49),
(2563, '2520', '6969', 49),
(2564, '2580', '6969', 49),
(2565, '2640', '6969', 49),
(2566, '2700', '6969', 49),
(2567, '2760', '6969', 49),
(2568, '2820', '6969', 49),
(2569, '2880', '6969', 49),
(2570, '2940', '6969', 49),
(2571, '3000', '6969', 49),
(2572, '3060', '6969', 49),
(2573, '3120', '6969', 49),
(2574, '3180', '6969', 49),
(2575, '3240', '6969', 49),
(2576, '3300', '6969', 49),
(2577, '3360', '6969', 49),
(2578, '3420', '6969', 49),
(2579, '3480', '6969', 49),
(2580, '3540', '6969', 49),
(2581, '3600', '6969', 49),
(2582, '3660', '6969', 49),
(2583, '3720', '6969', 49),
(2584, '3780', '6969', 49),
(2585, '3840', '6969', 49),
(2586, '3900', '6969', 49),
(2587, '3960', '6969', 49),
(2588, '4020', '6969', 49),
(2589, '4080', '6969', 49),
(2590, '4140', '6969', 49),
(2591, '4200', '6969', 49),
(2592, '4260', '6969', 49),
(2593, '4320', '6969', 49),
(2594, '4380', '6969', 49),
(2595, '4440', '6969', 49),
(2596, '4500', '6969', 49),
(2597, '4560', '6969', 49),
(2598, '4620', '6969', 49),
(2599, '4680', '6969', 49),
(2600, '4740', '6969', 49),
(2601, '4800', '6969', 49),
(2602, '4860', '6969', 49),
(2603, '4920', '6969', 49),
(2604, '4980', '6969', 49),
(2605, '5040', '6969', 49),
(2606, '5100', '6969', 49),
(2607, '5160', '6969', 49),
(2608, '5220', '6969', 49),
(2609, '5280', '6969', 49),
(2610, '5340', '6969', 49),
(2611, '5400', '6969', 49),
(2612, '5460', '6969', 49),
(2613, '5520', '6969', 49),
(2614, '5580', '6969', 49),
(2615, '5640', '6969', 49),
(2616, '5700', '6969', 49),
(2617, '5760', '6969', 49),
(2618, '5820', '6969', 49),
(2619, '5880', '6969', 49),
(2620, '5940', '6969', 49),
(2621, '6000', '6969', 49),
(2622, '6060', '6969', 49),
(2623, '6120', '6969', 49),
(2624, '6180', '6969', 49),
(2625, '6240', '6969', 49),
(2626, '6300', '6969', 49),
(2627, '6360', '6969', 49),
(2628, '6420', '6969', 49),
(2629, '6480', '6969', 49),
(2630, '6540', '6969', 49),
(2631, '6600', '6969', 49),
(2632, '6660', '6969', 49),
(2633, '6720', '6969', 49),
(2634, '6780', '6969', 49),
(2635, '6840', '6969', 49),
(2636, '6900', '6969', 49),
(2637, '6960', '6969', 49),
(2638, '7020', '6969', 49),
(2639, '7080', '6969', 49),
(2640, '7140', '6969', 49),
(2641, '7200', '6969', 49),
(2642, '7260', '6969', 49),
(2643, '7320', '6969', 49),
(2644, '7380', '6969', 49),
(2645, '7440', '6969', 49),
(2646, '7500', '6969', 49),
(2647, '7560', '6969', 49),
(2648, '7620', '6969', 49),
(2649, '7680', '6969', 49),
(2650, '7740', '6969', 49),
(2651, '7800', '6969', 49),
(2652, '7860', '6969', 49),
(2653, '7920', '6969', 49),
(2654, '7980', '6969', 49),
(2655, '8040', '6969', 49),
(2656, '8100', '6969', 49),
(2657, '8160', '6969', 49),
(2658, '8220', '6969', 49),
(2659, '8280', '6969', 49),
(2660, '8340', '6969', 49),
(2661, '8400', '6969', 49),
(2662, '8460', '6969', 49),
(2663, '8520', '6969', 49),
(2664, '8580', '6969', 49),
(2665, '8640', '6969', 49),
(2666, '8700', '6969', 49),
(2667, '8760', '6969', 49),
(2668, '8820', '6969', 49),
(2669, '8880', '6969', 49),
(2670, '60', '6969', 52),
(2671, '120', '6969', 52),
(2672, '180', '6969', 52),
(2673, '240', '6969', 52),
(2674, '300', '6969', 52),
(2675, '360', '6969', 52),
(2676, '420', '6969', 52),
(2677, '480', '6969', 52),
(2678, '540', '6969', 52),
(2679, '600', '6969', 52),
(2680, '660', '6969', 52),
(2681, '720', '6969', 52),
(2682, '780', '6969', 52),
(2683, '840', '6969', 52),
(2684, '900', '6969', 52),
(2685, '960', '6969', 52),
(2686, '1020', '6969', 52),
(2687, '1080', '6969', 52),
(2688, '1140', '6969', 52),
(2689, '1200', '6969', 52),
(2690, '1260', '6969', 52),
(2691, '1320', '6969', 52),
(2692, '1380', '6969', 52),
(2693, '1440', '6969', 52),
(2694, '1500', '6969', 52),
(2695, '1560', '6969', 52),
(2696, '1620', '6969', 52),
(2697, '1680', '6969', 52),
(2698, '1740', '6969', 52),
(2699, '1800', '6969', 52),
(2700, '1860', '6969', 52),
(2701, '1920', '6969', 52),
(2702, '1980', '6969', 52),
(2703, '2040', '6969', 52),
(2704, '2100', '6969', 52),
(2705, '2160', '6969', 52),
(2706, '2220', '6969', 52),
(2707, '2280', '6969', 52),
(2708, '2340', '6969', 52),
(2709, '2400', '6969', 52),
(2710, '2460', '6969', 52),
(2711, '2520', '6969', 52),
(2712, '2580', '6969', 52),
(2713, '2640', '6969', 52),
(2714, '2700', '6969', 52),
(2715, '2760', '6969', 52),
(2716, '2820', '6969', 52),
(2717, '2880', '6969', 52),
(2718, '2940', '6969', 52),
(2719, '3000', '6969', 52),
(2720, '3060', '6969', 52),
(2721, '3120', '6969', 52),
(2722, '3180', '6969', 52),
(2723, '3240', '6969', 52),
(2724, '3300', '6969', 52),
(2725, '3360', '6969', 52),
(2726, '3420', '6969', 52),
(2727, '3480', '6969', 52),
(2728, '3540', '6969', 52),
(2729, '3600', '6969', 52),
(2730, '3660', '6969', 52),
(2731, '3720', '6969', 52),
(2732, '3780', '6969', 52),
(2733, '3840', '6969', 52),
(2734, '3900', '6969', 52),
(2735, '3960', '6969', 52),
(2736, '4020', '6969', 52),
(2737, '4080', '6969', 52),
(2738, '4140', '6969', 52),
(2739, '4200', '6969', 52),
(2740, '4260', '6969', 52),
(2741, '4320', '6969', 52),
(2742, '4380', '6969', 52),
(2743, '4440', '6969', 52),
(2744, '4500', '6969', 52),
(2745, '4560', '6969', 52),
(2746, '4620', '6969', 52),
(2747, '4680', '6969', 52),
(2748, '4740', '6969', 52),
(2749, '4800', '6969', 52),
(2750, '4860', '6969', 52),
(2751, '4920', '6969', 52),
(2752, '4980', '6969', 52),
(2753, '5040', '6969', 52),
(2754, '5100', '6969', 52),
(2755, '5160', '6969', 52),
(2756, '5220', '6969', 52),
(2757, '5280', '6969', 52),
(2758, '5340', '6969', 52),
(2759, '5400', '6969', 52),
(2760, '5460', '6969', 52),
(2761, '5520', '6969', 52),
(2762, '5580', '6969', 52),
(2763, '5640', '6969', 52),
(2764, '5700', '6969', 52),
(2765, '5760', '6969', 52),
(2766, '5820', '6969', 52),
(2767, '5880', '6969', 52),
(2768, '5940', '6969', 52),
(2769, '6000', '6969', 52),
(2770, '6060', '6969', 52),
(2771, '6120', '6969', 52),
(2772, '6180', '6969', 52),
(2773, '6240', '6969', 52),
(2774, '6300', '6969', 52),
(2775, '6360', '6969', 52),
(2776, '6420', '6969', 52),
(2777, '6480', '6969', 52),
(2778, '6540', '6969', 52),
(2779, '6600', '6969', 52),
(2780, '6660', '6969', 52),
(2781, '6720', '6969', 52),
(2782, '6780', '6969', 52),
(2783, '6840', '6969', 52),
(2784, '6900', '6969', 52),
(2785, '6960', '6969', 52),
(2786, '7020', '6969', 52),
(2787, '7080', '6969', 52),
(2788, '7140', '6969', 52),
(2789, '7200', '6969', 52),
(2790, '7260', '6969', 52),
(2791, '7320', '6969', 52),
(2792, '7380', '6969', 52),
(2793, '7440', '6969', 52),
(2794, '7500', '6969', 52),
(2795, '7560', '6969', 52),
(2796, '7620', '6969', 52),
(2797, '7680', '6969', 52),
(2798, '7740', '6969', 52),
(2799, '7800', '6969', 52),
(2800, '7860', '6969', 52),
(2801, '7920', '6969', 52),
(2802, '7980', '6969', 52),
(2803, '8040', '6969', 52),
(2804, '8100', '6969', 52),
(2805, '8160', '6969', 52),
(2806, '8220', '6969', 52),
(2807, '8280', '6969', 52),
(2808, '8340', '6969', 52),
(2809, '8400', '6969', 52),
(2810, '8460', '6969', 52),
(2811, '8520', '6969', 52),
(2812, '8580', '6969', 52),
(2813, '8640', '6969', 52),
(2814, '8700', '6969', 52),
(2815, '8760', '6969', 52),
(2816, '8820', '6969', 52),
(2817, '8880', '6969', 52);

-- --------------------------------------------------------

--
-- Table structure for table `measurements_device`
--

CREATE TABLE `measurements_device` (
  `id` int(11) NOT NULL,
  `company` varchar(127) CHARACTER SET utf8 NOT NULL,
  `model` varchar(127) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `measurements_device`
--

INSERT INTO `measurements_device` (`id`, `company`, `model`) VALUES
(1, 'Agilant', 'NMR'),
(2, 'Agilant', 'NMR');

-- --------------------------------------------------------

--
-- Table structure for table `measurements_measurement`
--

CREATE TABLE `measurements_measurement` (
  `id` int(11) NOT NULL,
  `file` varchar(100) CHARACTER SET utf8 NOT NULL,
  `is_approved` longtext CHARACTER SET utf8 NOT NULL,
  `device_id` longtext CHARACTER SET utf8 NOT NULL,
  `experiment_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `measurements_measurement`
--

INSERT INTO `measurements_measurement` (`id`, `file`, `is_approved`, `device_id`, `experiment_id`) VALUES
(49, 'testing_milad_csv_to_upload.csv', '1', '1', 90),
(50, 'testing_milad_csv_to_upload.csv', '1', '1', 90),
(51, 'testing_milad_csv_to_upload.csv', '1', '1', 90),
(52, 'testin_1.csv', '1', '1', 90);

-- --------------------------------------------------------

--
-- Table structure for table `NMR_data`
--

CREATE TABLE `NMR_data` (
  `id` int(11) NOT NULL,
  `measurement` longtext CHARACTER SET utf8 NOT NULL,
  `res_time` longtext CHARACTER SET utf8 NOT NULL,
  `percent_conversion` longtext CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `socialaccount_socialaccount`
--

CREATE TABLE `socialaccount_socialaccount` (
  `id` int(11) NOT NULL,
  `provider` varchar(30) CHARACTER SET utf8 NOT NULL,
  `uid` varchar(191) CHARACTER SET utf8 NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  `user_id` longtext CHARACTER SET utf8 NOT NULL,
  `extra_data` longtext CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `socialaccount_socialapp`
--

CREATE TABLE `socialaccount_socialapp` (
  `id` int(11) NOT NULL,
  `provider` varchar(30) CHARACTER SET utf8 NOT NULL,
  `name` varchar(40) CHARACTER SET utf8 NOT NULL,
  `client_id` varchar(191) CHARACTER SET utf8 NOT NULL,
  `key` varchar(191) CHARACTER SET utf8 NOT NULL,
  `secret` varchar(191) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `socialaccount_socialapp_sites`
--

CREATE TABLE `socialaccount_socialapp_sites` (
  `id` int(11) NOT NULL,
  `socialapp_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `socialaccount_socialtoken`
--

CREATE TABLE `socialaccount_socialtoken` (
  `id` int(11) NOT NULL,
  `token` longtext CHARACTER SET utf8 NOT NULL,
  `token_secret` longtext CHARACTER SET utf8 NOT NULL,
  `expires_at` datetime DEFAULT NULL,
  `account_id` int(11) NOT NULL,
  `app_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `sqlite_sequence`
--

CREATE TABLE `sqlite_sequence` (
  `name` longtext CHARACTER SET utf8 DEFAULT NULL,
  `seq` longtext CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `sqlite_sequence`
--

INSERT INTO `sqlite_sequence` (`name`, `seq`) VALUES
('django_migrations', '33'),
('django_content_type', '28'),
('auth_permission', '112'),
('auth_group', '0'),
('users_group', '1'),
('account_emailaddress', '3'),
('django_admin_log', '3'),
('experiments_reactor', '0'),
('experiments_experiment_chemicals', '2'),
('experiments_experiment', '3'),
('experiments_inventory', '1'),
('django_site', '1'),
('socialaccount_socialapp', '0'),
('socialaccount_socialaccount', '0'),
('users_user', '3'),
('users_country', '252'),
('users_institution', '1'),
('users_institution_groups', '1'),
('users_user_group', '1'),
('chemicals_inchi', '2'),
('chemicals_name', '20'),
('chemicals_cas', '1'),
('chemicals_smiles', '1'),
('experiments_company', '2');

-- --------------------------------------------------------

--
-- Table structure for table `users_country`
--

CREATE TABLE `users_country` (
  `id` int(11) NOT NULL,
  `code` varchar(2) CHARACTER SET utf8 NOT NULL,
  `name` varchar(60) CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users_country`
--

INSERT INTO `users_country` (`id`, `code`, `name`) VALUES
(1, 'AF', 'Afghanistan'),
(2, 'AX', 'Aland Islands'),
(3, 'AL', 'Albania'),
(4, 'DZ', 'Algeria'),
(5, 'AS', 'American Samoa'),
(6, 'AD', 'Andorra'),
(7, 'AO', 'Angola'),
(8, 'AI', 'Anguilla'),
(9, 'AQ', 'Antarctica'),
(10, 'AG', 'Antigua and Barbuda'),
(11, 'AR', 'Argentina'),
(12, 'AM', 'Armenia'),
(13, 'AW', 'Aruba'),
(14, 'AU', 'Australia'),
(15, 'AT', 'Austria'),
(16, 'AZ', 'Azerbaijan'),
(17, 'BS', 'Bahamas'),
(18, 'BH', 'Bahrain'),
(19, 'BD', 'Bangladesh'),
(20, 'BB', 'Barbados'),
(21, 'BY', 'Belarus'),
(22, 'BE', 'Belgium'),
(23, 'BZ', 'Belize'),
(24, 'BJ', 'Benin'),
(25, 'BM', 'Bermuda'),
(26, 'BT', 'Bhutan'),
(27, 'BO', 'Bolivia'),
(28, 'BQ', 'Bonaire, Sint Eustatius and Saba'),
(29, 'BA', 'Bosnia and Herzegovina'),
(30, 'BW', 'Botswana'),
(31, 'BV', 'Bouvet Island'),
(32, 'BR', 'Brazil'),
(33, 'IO', 'British Indian Ocean Territory'),
(34, 'BN', 'Brunei Darussalam'),
(35, 'BG', 'Bulgaria'),
(36, 'BF', 'Burkina Faso'),
(37, 'BI', 'Burundi'),
(38, 'KH', 'Cambodia'),
(39, 'CM', 'Cameroon'),
(40, 'CA', 'Canada'),
(41, 'CV', 'Cape Verde'),
(42, 'KY', 'Cayman Islands'),
(43, 'CF', 'Central African Republic'),
(44, 'TD', 'Chad'),
(45, 'CL', 'Chile'),
(46, 'CN', 'China'),
(47, 'CX', 'Christmas Island'),
(48, 'CC', 'Cocos (Keeling) Islands'),
(49, 'CO', 'Colombia'),
(50, 'KM', 'Comoros');

-- --------------------------------------------------------

--
-- Table structure for table `users_group`
--

CREATE TABLE `users_group` (
  `id` int(11) NOT NULL,
  `name` varchar(60) CHARACTER SET utf8 NOT NULL,
  `short_name` varchar(10) CHARACTER SET utf8 NOT NULL,
  `is_private` longtext CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users_group`
--

INSERT INTO `users_group` (`id`, `name`, `short_name`, `is_private`) VALUES
(1, 'Polymer Reaction Design', 'PRD', '1');

-- --------------------------------------------------------

--
-- Table structure for table `users_institution`
--

CREATE TABLE `users_institution` (
  `id` int(11) NOT NULL,
  `name` varchar(127) CHARACTER SET utf8 NOT NULL,
  `short_name` varchar(20) CHARACTER SET utf8 NOT NULL,
  `country_id` longtext CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users_institution`
--

INSERT INTO `users_institution` (`id`, `name`, `short_name`, `country_id`) VALUES
(1, 'Monash University', 'Monash Uni', '14');

-- --------------------------------------------------------

--
-- Table structure for table `users_institution_groups`
--

CREATE TABLE `users_institution_groups` (
  `id` int(11) NOT NULL,
  `institution_id` longtext CHARACTER SET utf8 NOT NULL,
  `group_id` longtext CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users_institution_groups`
--

INSERT INTO `users_institution_groups` (`id`, `institution_id`, `group_id`) VALUES
(1, '1', '1');

-- --------------------------------------------------------

--
-- Table structure for table `users_user`
--

CREATE TABLE `users_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) CHARACTER SET utf8 NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `email` varchar(60) CHARACTER SET utf8 NOT NULL,
  `first_name` varchar(30) CHARACTER SET utf8 NOT NULL,
  `last_name` varchar(30) CHARACTER SET utf8 NOT NULL,
  `orcid` varchar(19) CHARACTER SET utf8 NOT NULL,
  `date_created` datetime NOT NULL,
  `is_private` longtext CHARACTER SET utf8 NOT NULL,
  `is_active` longtext CHARACTER SET utf8 NOT NULL,
  `is_staff` longtext CHARACTER SET utf8 NOT NULL,
  `is_superuser` longtext CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users_user`
--

INSERT INTO `users_user` (`id`, `password`, `last_login`, `email`, `first_name`, `last_name`, `orcid`, `date_created`, `is_private`, `is_active`, `is_staff`, `is_superuser`) VALUES
(1, 'pbkdf2_sha256$390000$pllvfL7n5yC2T6H8IirK6r$ie2mhCFycXUsLjgANHtxqfFBHr3dWMMTAsfgnFHNtCY=', '2022-10-11 10:40:24', 'mnem0001@student.monash.edu', 'Milad', 'Nemati', '', '2022-08-23 06:28:53', '1', '1', '1', '1'),
(2, 'pbkdf2_sha256$390000$vtj6fTp22IZfOeCxbDP8kK$ToBhyj+9Q2Nyy20wkv0HjZutNN192M31FuLpfgXrk1s=', NULL, 'arshiaadouli@gmail.com', 'Arshia', 'Adouli', '', '2022-08-26 11:18:21', '1', '1', '0', '0'),
(3, 'pbkdf2_sha256$390000$mgTctssHOkh0KMh8R65u20$QIAl0+Y3a3Y2QZyrB0CE5PAAr2TiIQeMKCHFIZRSdaI=', NULL, 'aado0001@student.monash.edu', 'arshia', 'adouli', '', '2022-08-26 11:19:43', '1', '1', '0', '0');

-- --------------------------------------------------------

--
-- Table structure for table `users_user_group`
--

CREATE TABLE `users_user_group` (
  `id` int(11) NOT NULL,
  `is_leader` longtext CHARACTER SET utf8 NOT NULL,
  `group_id` longtext CHARACTER SET utf8 NOT NULL,
  `user_id` longtext CHARACTER SET utf8 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users_user_group`
--

INSERT INTO `users_user_group` (`id`, `is_leader`, `group_id`, `user_id`) VALUES
(1, '1', '1', '1');

-- --------------------------------------------------------

--
-- Table structure for table `users_user_groups`
--

CREATE TABLE `users_user_groups` (
  `id` int(11) NOT NULL,
  `user_id` longtext CHARACTER SET utf8 NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `users_user_user_permissions`
--

CREATE TABLE `users_user_user_permissions` (
  `id` int(11) NOT NULL,
  `user_id` longtext CHARACTER SET utf8 NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account_emailaddress`
--
ALTER TABLE `account_emailaddress`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sqlite_autoindex_account_emailaddress_1` (`email`);

--
-- Indexes for table `account_emailconfirmation`
--
ALTER TABLE `account_emailconfirmation`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sqlite_autoindex_account_emailconfirmation_1` (`key`),
  ADD KEY `account_emailconfirmation_email_address_id_5b7f8c58` (`email_address_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sqlite_autoindex_auth_group_1` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`),
  ADD KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  ADD KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`);

--
-- Indexes for table `chemicals_cas`
--
ALTER TABLE `chemicals_cas`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `chemicals_inchi`
--
ALTER TABLE `chemicals_inchi`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sqlite_autoindex_chemicals_inchi_1` (`inchi_key`);

--
-- Indexes for table `chemicals_name`
--
ALTER TABLE `chemicals_name`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `chemicals_smiles`
--
ALTER TABLE `chemicals_smiles`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD UNIQUE KEY `sqlite_autoindex_django_session_1` (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `django_site`
--
ALTER TABLE `django_site`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sqlite_autoindex_django_site_1` (`domain`);

--
-- Indexes for table `experiments_company`
--
ALTER TABLE `experiments_company`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `experiments_experiment`
--
ALTER TABLE `experiments_experiment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `experiments_experiment_chemicals`
--
ALTER TABLE `experiments_experiment_chemicals`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `experiments_inventory`
--
ALTER TABLE `experiments_inventory`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `experiments_reactor`
--
ALTER TABLE `experiments_reactor`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `measurements_data`
--
ALTER TABLE `measurements_data`
  ADD PRIMARY KEY (`id`),
  ADD KEY `measurement_id` (`measurement_id`);

--
-- Indexes for table `measurements_device`
--
ALTER TABLE `measurements_device`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `measurements_measurement`
--
ALTER TABLE `measurements_measurement`
  ADD PRIMARY KEY (`id`),
  ADD KEY `experiment_id` (`experiment_id`);

--
-- Indexes for table `NMR_data`
--
ALTER TABLE `NMR_data`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `socialaccount_socialaccount`
--
ALTER TABLE `socialaccount_socialaccount`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `socialaccount_socialaccount_provider_uid_fc810c6e_uniq` (`provider`,`uid`);

--
-- Indexes for table `socialaccount_socialapp`
--
ALTER TABLE `socialaccount_socialapp`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `socialaccount_socialapp_sites`
--
ALTER TABLE `socialaccount_socialapp_sites`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `socialaccount_socialapp_sites_socialapp_id_site_id_71a9a768_uniq` (`socialapp_id`,`site_id`),
  ADD KEY `socialaccount_socialapp_sites_site_id_2579dee5` (`site_id`),
  ADD KEY `socialaccount_socialapp_sites_socialapp_id_97fb6e7d` (`socialapp_id`);

--
-- Indexes for table `socialaccount_socialtoken`
--
ALTER TABLE `socialaccount_socialtoken`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `socialaccount_socialtoken_app_id_account_id_fca4e0ac_uniq` (`app_id`,`account_id`),
  ADD KEY `socialaccount_socialtoken_app_id_636a42d7` (`app_id`),
  ADD KEY `socialaccount_socialtoken_account_id_951f210e` (`account_id`);

--
-- Indexes for table `users_country`
--
ALTER TABLE `users_country`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users_group`
--
ALTER TABLE `users_group`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users_institution`
--
ALTER TABLE `users_institution`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users_institution_groups`
--
ALTER TABLE `users_institution_groups`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users_user`
--
ALTER TABLE `users_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sqlite_autoindex_users_user_1` (`email`);

--
-- Indexes for table `users_user_group`
--
ALTER TABLE `users_user_group`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users_user_groups`
--
ALTER TABLE `users_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD KEY `users_user_groups_group_id_9afc8d0e` (`group_id`);

--
-- Indexes for table `users_user_user_permissions`
--
ALTER TABLE `users_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `users_user_user_permissions_permission_id_0b93982e` (`permission_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `experiments_experiment`
--
ALTER TABLE `experiments_experiment`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=91;

--
-- AUTO_INCREMENT for table `measurements_data`
--
ALTER TABLE `measurements_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2818;

--
-- AUTO_INCREMENT for table `measurements_measurement`
--
ALTER TABLE `measurements_measurement`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT for table `NMR_data`
--
ALTER TABLE `NMR_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `experiments_experiment`
--
ALTER TABLE `experiments_experiment`
  ADD CONSTRAINT `experiments_experiment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users_user` (`id`);

--
-- Constraints for table `measurements_data`
--
ALTER TABLE `measurements_data`
  ADD CONSTRAINT `measurements_data_ibfk_1` FOREIGN KEY (`measurement_id`) REFERENCES `measurements_measurement` (`id`);

--
-- Constraints for table `measurements_measurement`
--
ALTER TABLE `measurements_measurement`
  ADD CONSTRAINT `measurements_measurement_ibfk_1` FOREIGN KEY (`experiment_id`) REFERENCES `experiments_experiment` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
