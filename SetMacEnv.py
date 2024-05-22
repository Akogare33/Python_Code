import os
limit_maxfiles_plist='''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
    "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
    <dict>
        <key>Label</key>
        <string>limit.maxfiles</string>
        <key>ProgramArguments</key>
        <array>
            <string>launchctl</string>
            <string>limit</string>
            <string>maxfiles</string>
            <string>65536</string>
            <string>524288</string>
        </array>
        <key>RunAtLoad</key>
        <true/>
        <key>ServiceIPC</key>
        <false/>
    </dict>
</plist>
'''
with open('/Library/LaunchDaemons/limit.maxfiles.plist', 'w') as f:
    f.write(limit_maxfiles_plist)

os.chown('/Library/LaunchDaemons/limit.maxfiles.plist', 0, 0)

os.chmod('/Library/LaunchDaemons/limit.maxfiles.plist', 0o644)

os.system('sudo launchctl load -w /Library/LaunchDaemons/limit.maxfiles.plist')

os.system('launchctl limit maxfiles')