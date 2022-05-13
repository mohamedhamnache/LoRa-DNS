# LoRaWAN Handover Roaming 
LoRaWAN Handover Roaming is novel LoRaWAN roaming scheme to enable inter-operatorroaming based on DNS resolution and end-device context migration between networks. In this work, Our contributions are threefold :

* Design and implementation of a LoRaWAN architecture extension to handle inter-operators roaming capability.
* End-devices lookup DNS-based resolution using JoinEUI codification.
* Real Deployment roaming testbed

# LoRaWAN Architecture Extension
We extended the LoRaWAN standard architedture with two main components as illustrated in the following figure.

* Master Agent (MA) : The MA is a core component that plays an intermediary role between several independent LoRaWAN networks  owned by different operators.
* Local Agent (LA) : The LA is a local component connected to the Network Server

<p align="center">
<img src="./assets/roaming_arch_v3.png" alt="drawing" />
</p>

In More detail, each component is composed of serveral sub-components as described in the following figure.


<p align="center">
<img src="./assets/system-arch.png" alt="drawing" width="400"/>
</p>


# Experimental Setup
To validate the designed solution for LoRaWAN handover roaming , we implemented and deployed a testbed based on [ChirpStack](https://www.chirpstack.io/)
<p align="center">
<img src="./assets/setup.jpg" alt="drawing" width="400"/>
</p>




# Citation
```
@INPROCEEDINGS{9524996,
  author={Hamnache, Mohamed and Kacimi, Rahim and Beylot, André-Luc},
  booktitle={2021 IEEE 46th Conference on Local Computer Networks (LCN)}, 
  title={Unifying LoRaWAN Networks by Enabling the Roaming Capability}, 
  year={2021},
  volume={},
  number={},
  pages={371-374},
  doi={10.1109/LCN52139.2021.9524996}}
```

