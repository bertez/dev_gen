import os
import sys
import argparse
import pkg_resources


class DevGenerator(object):
    def __init__(self, name, repo, type):
        basedir = '/Users/berto/Projects/www/{0}'

        templates = {
            'default': 'default.template',
            'phpcan': 'default.phpcan.template',
            'laravel': 'default.laravel.template'
        }

        template = templates[type]


        # setup directories and names
        self.name = name
        self.repo = repo
        self.targetdir = basedir.format(self.name)
        self.confdir = basedir.format('conf/')

        # load template
        self.template = pkg_resources.resource_string('resources', template)
        # replace template
        self.conf = self.template.format(name=self.name)
        self.type = type

    def createDev(self):
        # Check if folder exists

        if os.path.isdir(self.targetdir) or os.path.isfile(self.confdir + self.name):
            print 'Error: folder or configuration file already exists'
            sys.exit(2)

        # Create folder in place
        try:
            print '...Creating folder'
            os.makedirs(self.targetdir)
        except:
            print 'Error creating folder :('
            sys.exit(2)

        # create file in conf folder
        try:
            print '...Writing nginx configuration'
            with open(self.confdir + self.name, 'w') as f:
                f.write(self.conf)
        except:
            print 'Error creating conf file :('
            sys.exit(2)

    def updateRepo(self):
        gitRepos = ['github', 'gitlab']

        command = 'git clone {0} {1}' if any(repo in self.repo for repo in gitRepos) else 'svn co {0} {1}'

        change_permissions = False

        # execute checkout/clone
        try:
            os.system(command.format(self.repo, self.targetdir))
            change_permissions = True
        except:
            print 'Error updating the repo, please do it manually'

        if change_permissions and self.type == 'phpcan':
            # change permissions
            writable_folders = ['/phpcan/cache', '/phpcan/logs',
                                '/web/uploads', '/web/cache']
            for folder in writable_folders:
                directory = self.targetdir + folder
                if not os.path.exists(directory):
                    os.makedirs(directory)
                os.chmod(directory, 0777)

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
    parser.add_argument('--template', action='store', dest='template', default='default', choices=['default', 'phpcan', 'laravel'], help='Type of framework')

    arguments = parser.parse_args()

    d = DevGenerator(arguments.name, arguments.repo, arguments.template)

    print 'Creating new development environment'
    d.createDev()

    if arguments.repo:
        print 'Checking out repository'
        d.updateRepo()

    d.restartServer()
