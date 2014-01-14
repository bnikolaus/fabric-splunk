from fabric.api import *
import getpass

# Read the docs before deploying
# http://docs.splunk.com/Documentation/Splunk/6.0.1/Forwarding/Setupforwardingandreceiving

forwarder_version='splunkforwarder-6.0.1-189883-Linux-x86_64.tgz'
splunk_version='splunk-6.0.1-189883-Linux-x86_64.tgz'

# Change the password
password='Password1' 

env.user ='root'

#env.parallel = 'True'
#env.password = getpass.getpass('Enter passwords: ')

with open("forwarder.list") as f:
    env.roledefs['forwarder'] = f.readlines()

@roles('forwarder')
def setup():
    ''' Deployes a splunk forwarder with base setup ''' 
     
    put(forwarder_version, '/tmp')
     
    run('tar -xvf /tmp/%s' % (forwarder_version) + ' -C /opt/')
    run('/opt/splunkforwarder/bin/splunk start --answer-yes --no-prompt --accept-license')
    run('/opt/splunkforwarder/bin/splunk enable boot-start')
    run(' /opt/splunkforwarder/bin/splunk edit user admin -password %s ' % (password) + ' -auth admin:changeme')

    # setup a input to watch 
    # run('/opt/splunkforwarder/bin/splunk add monitor /var/log/messages -sourcetype syslog')
    # this will modify /opt/splunkforwarder/etc/apps/search/local/inputs.conf
    
    # show what is being monitored on the server 
    # run('$SPLUNK_HOME/bin/splunk list monitor') 
    
    # oneshot
    # run('$SPLUNK_HOME/bin/splunk add oneshot /var/log/applog')


def destroy():
    ''' Destroy a deployed splunk forwarder ''' 
    run('$SPLUNK_HOME/bin/splunk stop')
    run('$SPLUNK_HOME/bin/splunk disable boot-start')
    run('rm -rf $SPLUNK_HOME')
    run('rm -rf /opt/splunkdata')
