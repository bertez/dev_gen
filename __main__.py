import os
import sys
import pwd
import grp
import argparse
import pkg_resources


class DevGenerator(object):
    def __init__(self, name, repo=None, ans=True):
        self.name = name
        self.repo = repo
        self.template = pkg_resources.resource_string('resources',
                                                      'default.template')
        self.basedir = '/Users/berto/Projects/ANS/{0}'
        self.targetdir = self.basedir.format(self.name)
        self.confdir = self.basedir.format('conf/')
        self.uid = pwd.getpwnam("berto").pw_uid
        self.gid = grp.getgrnam("_www").gr_gid
        # replace template
        self.conf = self.template.format(name=self.name)
        self.ans = ans

    def createDev(self):
        # Check if folder exists

        if os.path.isdir(self.targetdir):
            print 'Error: check the project name'
            sys.exit(2)

        # Create folder in place
        print '...Creating folder'
        os.makedirs(self.targetdir)

        # create file in conf folder
        # TODO: check if file exists!
        print '...Writing nginx configuration'
        with open(self.confdir + self.name, 'w') as f:
            f.write(self.conf)

        # Fix permissions/group
        #print 'Fixing permissions'
        #os.chown(self.targetdir, self.uid, self.gid)

        # restart nginx
        print '...Restarting nginx'

        restart_command = 'sudo launchctl {0} /Library/LaunchDaemons/homebrew.mxcl.nginx.plist'
        os.system(restart_command.format('unload'))
        os.system(restart_command.format('load'))

        print
        print 'Everything should be OK'
        print 'http://{0}.dev'.format(self.name)

    def updateRepo(self):
        command = 'git clone {0} {1}' if 'github.com' in self.repo else 'svn co {0} {1}'

        #execute checkout/clone
        os.system(command.format(self.repo, self.targetdir))

        if self.ans:
            #change permissions
            writabe_folders = ['/phpcan/cache', '/phpcan/logs',
                               '/web/uploads', '/web/cache']
            for folder in writabe_folders:
                os.chmod(self.targetdir, 777)


if __name__ == '__main__':
    #./dev_gen name --repo url

    parser = argparse.ArgumentParser(description='Create a development server')
    parser.add_argument('name', action='store')
    parser.add_argument('--repo', action='store', dest='repo')

    arguments = parser.parse_args()

    d = DevGenerator(arguments.name, arguments.repo)

    print 'Creating new development environment'
    #d.createDev()

    if arguments.repo:
        print 'Checking out repository'
        d.updateRepo()
