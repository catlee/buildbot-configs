# Some settings
$buildbotconfigs_repo = "http://hg.mozilla.org/build/buildbot-configs"
$buildbotcustom_repo = "http://hg.mozilla.org/build/buildbotcustom"
$buildtools_repo = "http://hg.mozilla.org/build/tools"
$buildbot_repo = "http://hg.mozilla.org/build/buildbot"

Exec { logoutput => on_failure }

class packages {
    case $operatingsystem {
        "Ubuntu","Debian": {
            exec {
                "update-apt": 
                    command => "/usr/bin/apt-get update";
            }
            package {
                "mercurial":
                    require => Exec["update-apt"],
                    ensure => latest;
                "git-core":
                    require => Exec["update-apt"],
                    ensure => latest;
                "libmysqlclient-dev":
                    require => Exec["update-apt"],
                    ensure => latest;
                "python":
                    require => Exec["update-apt"],
                    ensure => latest;
                "python-virtualenv":
                    require => [Exec["update-apt"], Package['python']],
                    ensure => latest;
                "python-dev":
                    require => [Exec["update-apt"], Package['python']],
                    ensure => latest;
                "make":
                    require => Exec["update-apt"],
                    ensure => latest;
            }
        }
    }
}

exec {
    "buildbot-configs":
        require => Package["mercurial"],
        command => "/usr/bin/hg clone http://hg.mozilla.org/build/buildbot-configs /home/vagrant/buildbot-configs",
        creates => "/home/vagrant/buildbot-configs",
        user => "vagrant";
}

define buildbotmaster($basedir, $role) {
    exec {
        "${name}-make":
            require => [Class["packages"], Exec["buildbot-configs"]],
            cwd => "/home/vagrant/buildbot-configs",
            user => "vagrant",
            creates => $basedir,
            timeout => 600,
            command => "/usr/bin/make -f Makefile.setup PYTHON=/usr/bin/python USE_DEV_MASTER=1 BASEDIR=$basedir ROLE=$role HTTP_PORT=8001 PB_PORT=7001 SSH_PORT=9001 MASTER_NAME=staging-master USER=vagrant";
    }
}

include packages
buildbotmaster {
    "build-master":
        role => "build",
        basedir => "/home/vagrant/build-master";
    "test-master":
        role => "tests",
        basedir => "/home/vagrant/test-master";
}
