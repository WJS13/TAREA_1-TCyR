-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: bq4g7mtwkj0six0fgwn4-mysql.services.clever-cloud.com:3306
-- Tiempo de generación: 24-06-2024 a las 04:03:05
-- Versión del servidor: 8.0.15-5
-- Versión de PHP: 8.2.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bq4g7mtwkj0six0fgwn4`
--
CREATE DATABASE IF NOT EXISTS `bq4g7mtwkj0six0fgwn4` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `bq4g7mtwkj0six0fgwn4`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Coeficientes_Bi`
--

CREATE TABLE `Coeficientes_Bi` (
  `Bi` decimal(5,2) DEFAULT NULL,
  `lambda1` decimal(6,4) DEFAULT NULL,
  `A1` decimal(6,4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `Coeficientes_Bi`
--

INSERT INTO `Coeficientes_Bi` (`Bi`, `lambda1`, `A1`) VALUES
(0.01, 0.1730, 1.0030),
(0.02, 0.2445, 1.0060),
(0.04, 0.3450, 1.0120),
(0.06, 0.4217, 1.0179),
(0.08, 0.4860, 1.0239),
(0.10, 0.5423, 1.0298),
(0.20, 0.7593, 1.0592),
(0.30, 0.9205, 1.0880),
(0.40, 1.0528, 1.1164),
(0.50, 1.1656, 1.1441),
(0.60, 1.2644, 1.1713),
(0.70, 1.3525, 1.1978),
(0.80, 1.4320, 1.2236),
(0.90, 1.5044, 1.2488),
(1.00, 1.5708, 1.2732),
(2.00, 2.0288, 1.4793),
(3.00, 2.2889, 1.6227),
(4.00, 2.4565, 1.7270),
(5.00, 2.5704, 1.7970),
(6.00, 2.6537, 1.8338),
(7.00, 2.7165, 1.8673),
(8.00, 2.7654, 1.8920),
(9.00, 2.8044, 1.9106),
(10.00, 2.8363, 1.9249),
(20.00, 2.9857, 1.9781),
(30.00, 3.0372, 1.9898),
(40.00, 3.0632, 1.9942),
(50.00, 3.0788, 1.9962),
(100.00, 3.1102, 1.9990),
(200.00, 3.1416, 2.0000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `datos_generales`
--

CREATE TABLE `datos_generales` (
  `id_datos` int(11) NOT NULL,
  `Diametro_pera` float NOT NULL,
  `Volumen` float NOT NULL,
  `masa` float NOT NULL,
  `Cp` float NOT NULL,
  `densidad` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `datos_generales`
--

INSERT INTO `datos_generales` (`id_datos`, `Diametro_pera`, `Volumen`, `masa`, `Cp`, `densidad`) VALUES
(1, 0.0636, 0.00013, 0.125, 3589, 961.538);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `resultados_1`
--

CREATE TABLE `resultados_1` (
  `id_resultados` int(11) NOT NULL,
  `Lambda_1` float NOT NULL,
  `Bi` float NOT NULL,
  `A_1` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `resultados_1`
--

INSERT INTO `resultados_1` (`id_resultados`, `Lambda_1`, `Bi`, `A_1`) VALUES
(1, 0.926669, 0.304663, 1.08932),
(2, 1.11703, 0.456939, 1.13217),
(3, 1.11695, 0.456871, 1.13215),
(4, 1.1244, 0.463479, 1.13398),
(5, 1.15364, 0.489394, 1.14116),
(6, 1.15677, 0.492171, 1.14193),
(7, 1.19295, 0.527679, 1.15163),
(8, 1.17944, 0.514008, 1.14791),
(9, 1.11826, 0.458035, 1.13248),
(10, 1.1623, 0.497073, 1.14329),
(11, 1.11165, 0.452176, 1.13085),
(12, 1.21669, 0.551712, 1.15817);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `resultados_2`
--

CREATE TABLE `resultados_2` (
  `id_resultados` int(11) NOT NULL,
  `tau` float NOT NULL,
  `alfa` float NOT NULL,
  `k` float NOT NULL,
  `h` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `resultados_2`
--

INSERT INTO `resultados_2` (`id_resultados`, `tau`, `alfa`, `k`, `h`) VALUES
(1, 0.0996344, 0.000000335847, 1.159, 11.1039),
(2, 0.102942, 0.000000173498, 0.598734, 8.6033),
(3, 0.113334, 0.000000127342, 0.439452, 6.3136),
(4, 0.119878, 0.000000101021, 0.348619, 5.08107),
(5, 0.127183, 0.0000000857417, 0.295891, 4.5537),
(6, 0.132856, 0.0000000746385, 0.257574, 3.9865),
(7, 0.138213, 0.0000000665553, 0.22968, 3.81124),
(8, 0.162014, 0.0000000682645, 0.235578, 3.80783),
(9, 0.19939, 0.0000000746782, 0.257712, 3.71198),
(10, 0.222563, 0.0000000750217, 0.258897, 4.04688),
(11, 0.273913, 0.0000000839369, 0.289663, 4.11883),
(12, 0.259171, 0.000000072801, 0.251233, 4.35876);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `Temperaturas`
--

CREATE TABLE `Temperaturas` (
  `idTemperaturas` int(11) NOT NULL,
  `T_amb` varchar(45) NOT NULL,
  `T_centro` varchar(45) NOT NULL,
  `T_sup` varchar(45) NOT NULL,
  `Hora` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `Temperaturas`
--

INSERT INTO `Temperaturas` (`idTemperaturas`, `T_amb`, `T_centro`, `T_sup`, `Hora`) VALUES
(1, '23.000', '-5.950', '-1.981', '2024-06-23 02:30:20'),
(2, '22.900', '-5.826', '-0.214', '2024-06-23 02:35:26'),
(3, '22.900', '-5.456', '0.083', '2024-06-23 02:40:31'),
(4, '23.000', '-5.212', '0.368', '2024-06-23 02:45:31'),
(5, '22.900', '-4.896', '0.872', '2024-06-23 02:50:31'),
(6, '22.900', '-4.679', '1.073', '2024-06-23 02:55:31'),
(7, '22.900', '-4.392', '1.636', '2024-06-23 03:00:31'),
(8, '23.100', '-3.518', '2.238', '2024-06-23 03:06:31'),
(9, '23.400', '-2.503', '2.568', '2024-06-23 03:11:31'),
(10, '23.100', '-1.488', '3.686', '2024-06-23 03:16:31'),
(11, '23.300', '-0.279', '4.286', '2024-06-23 03:21:31'),
(12, '23.400', '0.239', '5.545', '2024-06-23 03:26:31');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `datos_generales`
--
ALTER TABLE `datos_generales`
  ADD PRIMARY KEY (`id_datos`);

--
-- Indices de la tabla `resultados_1`
--
ALTER TABLE `resultados_1`
  ADD PRIMARY KEY (`id_resultados`);

--
-- Indices de la tabla `resultados_2`
--
ALTER TABLE `resultados_2`
  ADD PRIMARY KEY (`id_resultados`);

--
-- Indices de la tabla `Temperaturas`
--
ALTER TABLE `Temperaturas`
  ADD PRIMARY KEY (`idTemperaturas`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `datos_generales`
--
ALTER TABLE `datos_generales`
  MODIFY `id_datos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `resultados_1`
--
ALTER TABLE `resultados_1`
  MODIFY `id_resultados` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `resultados_2`
--
ALTER TABLE `resultados_2`
  MODIFY `id_resultados` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `Temperaturas`
--
ALTER TABLE `Temperaturas`
  MODIFY `idTemperaturas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
