import os 
import logging
def CheckEnviron():
    if os.environ.get('ANDROID_HOME','None') != "None" and os.environ.get('NDKROOT','None') != "None" :
        return 1
    else :
        return 0
    
def FixEnviron():
    user=os.getlogin()
    var1=f"C:\Users\{user}\AppData\Local\Android\Sdk"
    var2="D:\android-ndk-r21e"
    os.environ.setdefault('ANDROID_HOME', var1)
    os.environ.setdefault('NDKROOT', var2)

if __name__ == '__main__':
    try:
        res = CheckEnviron()
        if res:
            logging.info("'ANDROID_HOME' and 'NDKROOT' are both exist")
        else:
            logging.info('The variables are incomplete, trying fix it')
            FixEnviron()
    except Exception as e:
        print(e)


# print(os.getlogin())
# ANDROID_HOME C:\Users\v_yljeyang\AppData\Local\Android\Sdk
# NDKROOT D:\android-ndk-r21e