desktop_file = i18n.merge_file(
  input: 'com.github.hezral.doomed.desktop.in',
  output: 'com.github.hezral.doomed.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils,
    args: [desktop_file]
  )
endif

appstream_file = i18n.merge_file(
  input: 'com.github.hezral.doomed.appdata.xml.in',
  output: 'com.github.hezral.doomed.appdata.xml',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'metainfo')
)

appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util,
    args: ['validate', appstream_file]
  )
endif

install_data('com.github.hezral.doomed.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file', compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
endif

icon_sizes = ['16', '24', '32', '48', '64', '128']
foreach i : icon_sizes
    install_data(
        join_paths('icons', i + '.png'),
        rename: meson.project_name() + '.png',
        install_dir: join_paths(get_option ('datadir'), 'icons', 'hicolor', i + 'x' + i, 'apps')
    )
    install_data(
        join_paths('icons', i + '.svg'),
        rename: meson.project_name() + '.svg',
        install_dir: join_paths(get_option ('datadir'), 'icons', 'hicolor', i + 'x' + i + '@2', 'apps')
    )
endforeach

# scalable_dir = join_paths('hicolor', 'scalable', 'apps')
# install_data(
#   join_paths('icons', '128.svg'),
#   rename: meson.project_name() + '.svg',
#   install_dir: join_paths(get_option('datadir'), 'icons', scalable_dir)
# )


image_sizes = ['0', '1', '2', '3', '4', '5']
foreach i : image_sizes
    install_data(
        join_paths('images', i + '.png'),
        install_dir: join_paths(pkgdatadir, project_short_name, 'data', 'images')
    )
endforeach

install_data('application.css',
  install_dir: join_paths(pkgdatadir, project_short_name, 'data')
)

install_data('unf.mp3',
  install_dir: join_paths(pkgdatadir, project_short_name, 'data')
)

