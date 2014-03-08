notify { "Sup pi ppl?": }

notify { "Disable console over serial. https://github.com/lurch/rpi-serial-console": }
exec { "wget https://raw.github.com/lurch/rpi-serial-console/master/rpi-serial-console -O /usr/bin/rpi-serial-console":
  creates => "/usr/bin/rpi-serial-console",
  user => root,
}
exec { "chmod +x /usr/bin/rpi-serial-console":
  user => root,
}

package { 'python-smbus':
 ensure => installed,
}