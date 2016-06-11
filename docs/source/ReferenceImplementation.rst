RPyMostat Reference Implementation
==================================

My planned reference implementation of the system is:

-  RaspberryPi 2+ physical control unit - USB relay output for control, and
   a temperature sensor, connecting via WiFi.

   -  `DS18B20 <https://www.sparkfun.com/products/245>`__ temperature
      sensor using GPIO
   -  For system control, either a
      `PiFace <https://www.sparkfun.com/products/11772>`__ or a
      `Phidgets
      1014 <http://www.phidgets.com/products.php?product_id=1014>`__ USB
      4 relay kit, both of which I already have.

-  2x RaspberryPi Zero temperature sensors in other rooms, connecting via WiFi.

   -  `DS18B20 <https://www.sparkfun.com/products/245>`__ temperature
      sensor using GPIO

-  Engine, web UI and a third (USB OWFS) temperature input on my
   desktop computer.

   -  `DS18S20 <https://www.sparkfun.com/products/retired/8366>`__
      temperature sensor connected via
      `DS9490R <http://www.maximintegrated.com/en/products/comms/ibutton/DS9490R.html>`__
      usb-to-1-wire adapter