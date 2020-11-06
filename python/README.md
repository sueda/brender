# Project Brender: Blender Brender Panel
```
Author: Nick Weidner
Date:	11-6-2020
Version: 3.1.0
```

The **Brender Panel** is a simple Panel addon to Blender to bulk import animated objects, apply materials across large collections of objects, and more.

## Getting Started

These instructions will help you setup the Brender Panel in your Blender distribution. 

### Prerequisites

The current Brender distribution supports Blender >= 2.8. For older Blender versions check the legacy directory.

The only requirement to use the Brender Panel is the plugin script.

### Installation

There are two methods for setting up the Brender Panel

1. In Blender open Scripting -> Open blender_panel.py -> run

2. In Blender open Preferences -> Add-ons -> Install -> select blender_panel.py -> enable by checking the add on checkbox

The first method allows for easy debugging and editing, while the second allows the plugin to run at startup from now on.

## Usage

There are a number of features Blender has available.

The most common input is a directory of files following the naming scheme "OBJECTNAME_######", but many of Brender's features can be used without this input. 

