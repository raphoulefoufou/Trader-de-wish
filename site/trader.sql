-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost:3306
-- Généré le : mar. 14 avr. 2026 à 14:15
-- Version du serveur : 5.7.24
-- Version de PHP : 8.3.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `trader`
--

-- --------------------------------------------------------

--
-- Structure de la table `client`
--

CREATE TABLE `client` (
  `id` int(11) NOT NULL,
  `pseudo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `mdp` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `token` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `monnaie` int(11) DEFAULT NULL,
  `gain_realise` decimal(15,2) DEFAULT '0.00'
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `client`
--

INSERT INTO `client` (`id`, `pseudo`, `email`, `mdp`, `token`, `monnaie`, `gain_realise`) VALUES
(34, 'aaaaaaa', 'aaaaaa@aaaaa.aa', '$2y$10$hAYmqfrujxXX0TGQq3qkVePxwamJtVTIL8MVE315/VgZUTqWXDDFa', '66', 18655, '0.18');

-- --------------------------------------------------------

--
-- Structure de la table `marche`
--

CREATE TABLE `marche` (
  `ticker` varchar(10) NOT NULL,
  `nom` varchar(255) NOT NULL,
  `info` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `marche`
--

INSERT INTO `marche` (`ticker`, `nom`, `info`) VALUES
('000660.KS', 'SK Hynix Inc.', 'Deuxième plus grand fabricant de puces mémoire au monde, fournisseur clé de mémoires HBM pour l\'IA.'),
('005930.KS', 'Samsung Electronics', 'Leader mondial de l\'électronique dominant les marchés des écrans OLED, des téléviseurs et des puces mémoire.'),
('066570.KS', 'LG Electronics', 'Fabricant majeur d\'appareils électroménagers et reconnu pour son innovation dans les écrans OLED.'),
('0763.HK', 'ZTE Corporation', 'Équipementier télécom chinois majeur dans le déploiement des réseaux 5G et des solutions de fibre optique.'),
('0992.HK', 'Lenovo Group', 'Premier fabricant mondial d\'ordinateurs personnels (PC) proposant également serveurs et infrastructures de données.'),
('1810.HK', 'Xiaomi Corporation', 'Constructeur leader dans les smartphones, les objets connectés et récemment les véhicules électriques.'),
('AAPL', 'Apple Inc.', 'Leader mondial des produits technologiques de pointe, incluant l\'iPhone, le Mac et l\'iPad. L\'entreprise se diversifie massivement dans les services et les technologies portables.'),
('ADBE', 'Adobe Inc.', 'Spécialiste mondial des logiciels de création et de marketing numérique. Son écosystème Creative Cloud est la référence du secteur.'),
('AMD', 'Advanced Micro Devices Inc.', 'Concepteur et fabricant de semi-conducteurs spécialisé dans les microprocesseurs (CPU) et les cartes graphiques (GPU).'),
('AMZN', 'Amazon.com Inc.', 'Géant mondial du commerce en ligne et leader du cloud computing via AWS. Investit massivement dans l\'IA et la logistique.'),
('AVGO', 'Broadcom Inc.', 'Leader des solutions de semi-conducteurs et de logiciels d\'infrastructure pour les centres de données et les réseaux.'),
('BABA', 'Alibaba Group', 'Conglomérat chinois spécialisé dans le commerce électronique, la technologie et le cloud. Gère Taobao et Tmall.'),
('BIDU', 'Baidu Inc.', 'Le principal moteur de recherche en Chine, leader de l\'IA, de la conduite autonome (Apollo) et du cloud.'),
('CRM', 'Salesforce Inc.', 'Pionnier et leader mondial des solutions de gestion de la relation client (CRM) basées sur le cloud.'),
('CSCO', 'Cisco Systems Inc.', 'Leader mondial des technologies de réseau, de commutation, de routage et de sécurité informatique.'),
('DBX', 'Dropbox Inc.', 'Service de stockage et de partage de fichiers dans le cloud axé sur la collaboration et la synchronisation sécurisée.'),
('DELL', 'Dell Technologies Inc.', 'Fournisseur global de solutions allant des ordinateurs personnels aux serveurs d\'entreprise et au stockage.'),
('EBAY', 'eBay Inc.', 'Plateforme de commerce électronique spécialisée dans les enchères et la vente directe, notamment pour les objets de collection.'),
('GOOGL', 'Alphabet Inc. (Google)', 'Mère de Google, leader de la recherche, de la publicité et d\'Android. Investit dans l\'IA profonde via DeepMind.'),
('HPQ', 'HP Inc.', 'Spécialiste mondial des ordinateurs personnels (PC), des solutions d\'impression et de l\'impression 3D industrielle.'),
('INTC', 'Intel Corporation', 'L\'un des plus grands fabricants de semi-conducteurs au monde pour les ordinateurs personnels et les serveurs.'),
('META', 'Meta Platforms Inc.', 'Mère de Facebook, Instagram et WhatsApp. Leader des réseaux sociaux investissant massivement dans le métavers.'),
('MSFT', 'Microsoft Corporation', 'Géant dominant les logiciels (Windows, Office) et le cloud (Azure). Propriétaire de LinkedIn et GitHub.'),
('MU', 'Micron Technology Inc.', 'Spécialiste mondial des solutions de mémoire DRAM et NAND pour smartphones, ordinateurs et serveurs.'),
('NVDA', 'NVIDIA Corporation', 'Leader incontesté des processeurs graphiques (GPU) et moteur de la révolution de l\'intelligence artificielle générative.'),
('OKTA', 'Okta Inc.', 'Spécialiste de la gestion des identités et des accès permettant de sécuriser les connexions aux applications cloud.'),
('ORCL', 'Oracle Corporation', 'Leader mondial des logiciels de base de données et des applications d\'entreprise (ERP, HCM) via son infrastructure cloud.'),
('PDD', 'PDD Holdings Inc. (Pinduoduo)', 'Plateforme d\'e-commerce célèbre pour son modèle d\'achat groupé, opérant Pinduoduo et Temu à l\'international.'),
('PYPL', 'PayPal Holdings Inc.', 'Leader mondial des paiements numériques et du transfert d\'argent, gérant également l\'écosystème Venmo.'),
('QCOM', 'Qualcomm Inc.', 'Leader mondial des technologies sans fil et des processeurs Snapdragon. Détient les brevets essentiels pour la 5G.'),
('SAP', 'SAP SE', 'Leader européen des logiciels de gestion d\'entreprise (ERP) aidant à piloter les finances et la logistique via le cloud.'),
('SHOP', 'Shopify Inc.', 'Plateforme d\'e-commerce permettant aux marchands de créer et gérer leurs propres boutiques en ligne.'),
('SONY', 'Sony Group Corporation', 'Conglomérat leader dans le jeu vidéo (PlayStation), l\'électronique et les capteurs d\'image pour smartphones.'),
('TCEHY', 'Tencent Holdings', 'Géant technologique chinois, leader du jeu vidéo et des réseaux sociaux via WeChat, présent dans la fintech et le cloud.'),
('TEAM', 'Atlassian Corporation', 'Éditeur de logiciels de collaboration et de gestion de projet (Jira, Confluence, Trello) pour les équipes IT.'),
('TSLA', 'Tesla Inc.', 'Leader mondial des véhicules électriques, des batteries de stockage d\'énergie et de l\'énergie solaire.'),
('TSM', 'TSMC', 'Plus grande fonderie de semi-conducteurs au monde fabriquant les puces les plus avancées pour Apple, NVIDIA et AMD.'),
('UBER', 'Uber Technologies Inc.', 'Leader mondial du transport à la demande et de la livraison de repas (Uber Eats), investissant dans la logistique.'),
('WDAY', 'Workday Inc.', 'Fournisseur de solutions cloud pour la gestion financière et les ressources humaines des grandes entreprises.'),
('ZM', 'Zoom Video Communications', 'Leader des communications vidéo et de la collaboration à distance intégrant téléphone cloud et webinaires.');

-- --------------------------------------------------------

--
-- Structure de la table `portefeuille`
--

CREATE TABLE `portefeuille` (
  `id` int(11) NOT NULL,
  `pseudo_client` varchar(255) DEFAULT NULL,
  `ticker` varchar(20) DEFAULT NULL,
  `quantite` int(11) DEFAULT NULL,
  `prix_achat_moyen` decimal(15,4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `portefeuille`
--

INSERT INTO `portefeuille` (`id`, `pseudo_client`, `ticker`, `quantite`, `prix_achat_moyen`) VALUES
(5, 'aaaaaaa', '005930.KS', 2, '117.8100'),
(6, 'aaaaaaa', 'AAPL', 5, '222.0900');

-- --------------------------------------------------------

--
-- Structure de la table `transactions`
--

CREATE TABLE `transactions` (
  `id` int(11) NOT NULL,
  `pseudo_client` varchar(255) DEFAULT NULL,
  `ticker` varchar(20) DEFAULT NULL,
  `quantite` int(11) DEFAULT NULL,
  `prix_unitaire` decimal(15,4) DEFAULT NULL,
  `type_action` enum('ACHAT','VENTE') DEFAULT NULL,
  `date_transaction` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Déchargement des données de la table `transactions`
--

INSERT INTO `transactions` (`id`, `pseudo_client`, `ticker`, `quantite`, `prix_unitaire`, `type_action`, `date_transaction`) VALUES
(8, 'aaaaaaa', '005930.KS', 5, '117.8100', 'ACHAT', '2026-04-09 14:42:41'),
(9, 'aaaaaaa', '005930.KS', 3, '117.8700', 'VENTE', '2026-04-09 16:26:12'),
(10, 'aaaaaaa', 'AAPL', 5, '222.0900', 'ACHAT', '2026-04-12 15:42:54');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `pseudo` (`pseudo`);

--
-- Index pour la table `marche`
--
ALTER TABLE `marche`
  ADD PRIMARY KEY (`ticker`);

--
-- Index pour la table `portefeuille`
--
ALTER TABLE `portefeuille`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `pseudo_client` (`pseudo_client`,`ticker`),
  ADD KEY `ticker` (`ticker`);

--
-- Index pour la table `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `pseudo_client` (`pseudo_client`),
  ADD KEY `ticker` (`ticker`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `client`
--
ALTER TABLE `client`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT pour la table `portefeuille`
--
ALTER TABLE `portefeuille`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT pour la table `transactions`
--
ALTER TABLE `transactions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `portefeuille`
--
ALTER TABLE `portefeuille`
  ADD CONSTRAINT `portefeuille_ibfk_1` FOREIGN KEY (`ticker`) REFERENCES `marche` (`ticker`);

--
-- Contraintes pour la table `transactions`
--
ALTER TABLE `transactions`
  ADD CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`ticker`) REFERENCES `marche` (`ticker`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
