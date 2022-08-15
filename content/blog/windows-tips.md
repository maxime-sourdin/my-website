Title: Windows tips
Date: 2019:21:10 18:00
Authors: Maxime SOURDIN
Category: Windows
Tags: Tweaks
Summary: Setting Power/Domain/Cleaning on Windows

## Setting power mode

#### Ultimate Performance:

    powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61

#### High Performance:

    powercfg -duplicatescheme 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c

#### Balanced:

    powercfg -duplicatescheme 381b4222-f694-41f0-9685-ff5bb260df2e

#### Power saver:

    powercfg -duplicatescheme a1841308-3541-4fab-bc81-f71556f20b4a

## Joining domain

    @echo off
    NETDOM JOIN %computername% /domain:SIO.LOCAL /userD:sourdin.m /passwordD:xacten
    del domaine.bat
    shutdown -r -f -t 0