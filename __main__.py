import os
import sys
import argparse
import pkg_resources


class DevGenerator(object):
    def __init__(self, name, repo, nophpcan):
        basedir = '/Users/berto/Projects/www/{0}'

        if nophpcan:
            template = 'default.template'
        else:
            template = 'default.phpcan.template'

        #setup directories and names
        self.name = name
        self.repo = repo
        self.targetdir = basedir.format(self.name)
        self.confdir = basedir.format('conf/')

        #load template
        self.template = pkg_resources.resource_string('resources', template)

        # replace template
        self.conf = self.template.format(name=self.name)
        self.nophpcan = nophpcan

    def createDev(self):
        # Check if folder exists

        if os.path.isdir(self.targetdir) or os.path.isfile(self.confdir + self.name):
            print 'Error: folder or configuration file already exists'
            sys.exit(2)

        # Create folder in place
        print '...Creating folder'
        os.makedirs(self.targetdir)

        # create file in conf folder
        print '...Writing nginx configuration'
        with open(self.confdir + self.name, 'w') as f:
            f.write(self.conf)

    def updateRepo(self):
        command = 'git clone {0} {1}' if 'github.com' in self.repo else 'svn co {0} {1}'

        #execute checkout/clone
        os.system(command.format(self.repo, self.targetdir))

        if not self.nophpcan:
            #change permissions
            writable_folders = ['/phpcan/cache', '/phpcan/logs',
                                '/web/uploads', '/web/cache']
            for folder in writable_folders:
                os.chmod(self.targetdir + folder, 0777)

    def restartServer(self):
        # restart nginx
        print '...Restarting nginx'

        restart_command = 'sudo launchctl {0} /Library/LaunchDaemons/homebrew.mxcl.nginx.plist'
        os.system(restart_command.format('unload'))
        os.system(restart_command.format('load'))

        print
        print 'Everything should be OK'
        print 'http://{0}.dev'.format(self.name)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Create a local development server')
    parser.add_argument('name', action='store', help='Name of the environment')
    parser.add_argument('--repo', action='store', dest='repo', default=None, help='URL of the repo. Supports svn and github repos.')
    parser.add_argument('--nophpcan', action='store_true', dest='nophpcan',
                        default=False, help='Do not create phpcan rewrites')

    arguments = parser.parse_args()

    d = DevGenerator(arguments.name, arguments.repo, arguments.nophpcan)

    print 'Creating new development environment'
    d.createDev()

    if arguments.repo:
        print 'Checking out repository'
        d.updateRepo()

    d.restartServer()
