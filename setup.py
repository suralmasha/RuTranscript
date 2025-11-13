from pathlib import Path
from shutil import rmtree

import tomli
from setuptools import find_packages, setup

if __name__ == '__main__':
    with Path('pyproject.toml').open('rb') as f:
        pyproject = tomli.load(f)

    poetry_config = pyproject.get('tool', {}).get('poetry', {})

    project_name = poetry_config.get('name', 'ru_transcript')
    description = poetry_config.get('description', '')
    url = 'https://github.com/suralmasha/RuTranscript'

    version = '1.0.0'

    authors = poetry_config.get('authors', [])
    author_names = []
    author_emails = []
    for name_email in authors:
        name, email = name_email.split('<')
        author_names.append(name.strip())
        author_emails.append(email.replace('>', '').strip())
    author_names_str = ', '.join(author_names)
    author_emails_str = ', '.join(author_emails)

    install_requires = []
    dependencies = pyproject.get('project', {}).get('dependencies', [])
    for dep in dependencies:
        if isinstance(dep, str):
            install_requires.append(dep)
        elif isinstance(dep, dict):
            name = dep['name']
            if 'url' in dep:
                install_requires.append(f"{name} @ {dep['url']}")
            elif 'git' in dep:
                git_line = f"{name} @ git+{dep['git']}"
                if 'tag' in dep:
                    git_line += f"@{dep['tag']}"
                install_requires.append(git_line)

    sources_dir = './src'
    excluded_files = []

    setup(
        name=project_name,
        version=version,
        description=description,
        url=url,
        author=author_names_str,
        author_email=author_emails_str,
        install_requires=install_requires,
        packages=find_packages(sources_dir, excluded_files),
        package_dir={'': sources_dir},
    )

    rmtree('./src/RuTranscript.egg-info')
