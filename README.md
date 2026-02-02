## ZLT-X28 Firmware 1.5.13 + Unlock Guide

This repository contains:

* **Main firmware for ZLT-X28 (version 1.5.13)**
* **Unlock script**

> **All required files, including the unlock script, are provided in this repository.**
> You do NOT need to download anything from external sources.

---

## Firmware Installation

1. Log in to the modem web interface
2. Go to **System Update**
3. Upload the firmware file and start the update process
4. After updating, the modem will be **locked**

   * This is expected and will be fixed in later steps

---

## Obtain Network Access (IP Address)

After the modem boots, it must obtain an IP address.
The method does not matter:

* Configure WAN to get an IP
* Connect it to a phone
* Any other network source

The modem just needs network connectivity.

---

## Enable Telnet / SSH (Command Injection)

Before connecting via SSH or Telnet, you must perform a **command injection** through the **DMZ / Firewall** section.

### Inject the following value into the DMZ IP field:

```text
192.168.1.1 ; telnetd -l /bin/ash
```

Enter this exactly as shown in the DMZ IP field.

---

## Enable via API (Linux)

1. Open the browser developer tools:

   * Press `F12`
   * Go to the **Network** tab
   * Find and copy the `sessionId`
2. Run the following command on Linux and replace `<session id>` with the extracted value:

```bash
curl 'https://192.168.70.1/cgi-bin/http.cgi' \
--data-raw '{"enabled":"1","ip":"192.168.1.1 ; telnetd -l /bin/ash","cmd":172,"method":"POST","success":true,"subcmd":6,"token":"5948b69147b3850eee5e7266188934c5","language":"EN","sessionId":"<session id>"}' -k
```

After this step, Telnet and SSH will be available.

---

## Device Access (SSH)

SSH credentials:

* Port: `22`
* Username: `admin`
* Password: `admin`

> The device uses the deprecated `ssh-rsa` algorithm.
> You must explicitly allow it in your SSH client.

```bash
ssh -o HostKeyAlgorithms=+ssh-rsa admin@192.168.70.1
```

---

## Unlocking the Modem

1. **Download the unlock script from this repository x28 , x28tgz**
2. Copy the file to the modem (SCP, local web server, or any method you prefer)
3. Make the script executable:

```bash
chmod +x x28
```

4. Execute the script

```bash
sh x28
```

5. The modem will reboot
6. After boot, perform **one Factory Reset**

Done.

---

## Repository Link

📌 [https://github.com/mahdigh782/Unlock-ZLT-X28](https://github.com/mahdigh782/Unlock-ZLT-X28)

---
