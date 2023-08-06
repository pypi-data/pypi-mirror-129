require 'spec_helper'

describe 'panko::wsgi::apache' do

  shared_examples_for 'apache serving panko with mod_wsgi' do
    context 'with default parameters' do
      it { is_expected.to contain_class('panko::params') }
      it { is_expected.to contain_class('apache') }
      it { is_expected.to contain_class('apache::mod::wsgi') }
      it { is_expected.to contain_class('apache::mod::ssl') }
      it { is_expected.to contain_openstacklib__wsgi__apache('panko_wsgi').with(
        :bind_port           => 8977,
        :group               => 'panko',
        :path                => '/',
        :servername          => facts[:fqdn],
        :ssl                 => true,
        :threads             => 1,
        :user                => 'panko',
        :workers             => facts[:os_workers],
        :wsgi_daemon_process => 'panko',
        :wsgi_process_group  => 'panko',
        :wsgi_script_dir     => platform_params[:wsgi_script_path],
        :wsgi_script_file    => 'app',
        :wsgi_script_source  => '/usr/bin/panko-api',
        :access_log_file     => false,
        :access_log_format   => false,
      )}
    end

    context 'when overriding parameters using different ports' do
      let :params do
        {
          :servername                => 'dummy.host',
          :bind_host                 => '10.42.51.1',
          :port                      => 12345,
          :ssl                       => false,
          :wsgi_process_display_name => 'panko',
          :workers                   => 8,
          :custom_wsgi_process_options => {
            'python_path' => '/my/python/admin/path',
          },
          :access_log_file           => '/var/log/httpd/access_log',
          :access_log_format         => 'some format',
          :error_log_file            => '/var/log/httpd/error_log'
        }
      end
      it { is_expected.to contain_class('panko::params') }
      it { is_expected.to contain_class('apache') }
      it { is_expected.to contain_class('apache::mod::wsgi') }
      it { is_expected.to_not contain_class('apache::mod::ssl') }
      it { is_expected.to contain_openstacklib__wsgi__apache('panko_wsgi').with(
        :bind_host                 => '10.42.51.1',
        :bind_port                 => 12345,
        :group                     => 'panko',
        :path                      => '/',
        :servername                => 'dummy.host',
        :ssl                       => false,
        :threads                   => 1,
        :user                      => 'panko',
        :workers                   => 8,
        :wsgi_daemon_process       => 'panko',
        :wsgi_process_display_name => 'panko',
        :wsgi_process_group        => 'panko',
        :wsgi_script_dir           => platform_params[:wsgi_script_path],
        :wsgi_script_file          => 'app',
        :wsgi_script_source        => '/usr/bin/panko-api',
        :custom_wsgi_process_options => {
          'python_path'  => '/my/python/admin/path',
        },
        :access_log_file           => '/var/log/httpd/access_log',
        :access_log_format         => 'some format',
        :error_log_file            => '/var/log/httpd/error_log'
      )}
    end
  end

  on_supported_os({
    :supported_os   => OSDefaults.get_supported_os
  }).each do |os,facts|
    context "on #{os}" do
      let (:facts) do
        facts.merge!(OSDefaults.get_facts({
          :os_workers     => 4,
          :concat_basedir => '/var/lib/puppet/concat',
          :fqdn           => 'some.host.tld',
        }))
      end

      let(:platform_params) do
        case facts[:osfamily]
        when 'Debian'
          {
            :httpd_service_name => 'apache2',
            :httpd_ports_file   => '/etc/apache2/ports.conf',
            :wsgi_script_path   => '/usr/lib/cgi-bin/panko',
          }
        when 'RedHat'
          {
            :httpd_service_name => 'httpd',
            :httpd_ports_file   => '/etc/httpd/conf/ports.conf',
            :wsgi_script_path   => '/var/www/cgi-bin/panko',
          }
        end
      end

      it_behaves_like 'apache serving panko with mod_wsgi'
    end
  end
end
