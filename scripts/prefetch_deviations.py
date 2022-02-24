from decimal import Decimal as D
import logging
import json
from os import path
from typing import Dict, List
from brownie import CurveRegistryCache, interface  # type: ignore
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

OUTPUT_FILE = "build/deviations.json"
NEW_ORACLE_DEPLOYMENT_BLOCK = 17613381
BLOCK_INTERVAL = 3600 * 3 // 12  # 3 hours in blocks


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, D):
            return float(obj.quantize(D(10) ** -5))
        return json.JSONEncoder.default(self, obj)


CRV_USD = "0xf939E0A03FB07F59A73314E73794Be0E57ac1b4E"
CURVE_POOLS_ADDRESS = {
    "0xA5407eAE9Ba41422680e2e00537571bcC53efBfD",
    "0x5FAE7E604FC3e24fd43A72867ceBaC94c65b404A",
    "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7",
    "0x0f3159811670c117c372428D4E69AC32325e4D0F",
    "0xDcEF968d416a41Cdac0ED8702fAC8128A64241A2",
    "0x4DEcE678ceceb27446b35C672dC7d61F30bAD69E",
    "0x390f3595bCa2Df7d23783dFd126427CCeb997BF4",
    "0xDC24316b9AE028F1497c275EB9192a3Ea0f67022",
    "0x0CD6f267b2086bea681E922E19D40512511BE538",
    "0xd632f22692FaC7611d2AA1C0D552930D43CAEd3B",
    "0xCa978A0528116DDA3cbA9ACD3e68bc6191CA53D0",
    "0x5a6A4D54456819380173272A5E8E9B9904BdF41B",
    "0xaE34574AC03A15cd58A92DC79De7B1A0800F1CE3",
}


@dataclass
class Coin:
    address: str
    name: str
    decimals: int


class AssetType:
