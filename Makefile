TESTS=tests authtools
SETTINGS=tests.sqlite_test_settings
COVERAGE_COMMAND=python -Wa

# We download the tests from Django and then inherit from them. These environment variables are
# overridden by the tox.ini. If you are adding support for a new version of Django, you can find
# the checksum at https://www.djangoproject.com/m/pgp/Django-x.x.x.checksum.txt
DJANGO_VERSION?=3.1.7
DJANGO_CHECKSUM?=32ce792ee9b6a0cbbec340123e229ac9f765dff8c2a4ae9247a14b2ba3a365a7
SITE_PACKAGES?=./tests


test: test-builtin test-authtools test-customuser

test-builtin: auth_tests
	cd tests && $(COVERAGE_COMMAND) manage.py test --verbosity=2 --settings=$(SETTINGS) --traceback $(TESTS)

test-authtools: auth_tests
	+AUTH_USER_MODEL='authtools.User' make test-builtin

test-customuser: auth_tests
	+AUTH_USER_MODEL='tests.User' make test-builtin

coverage:
	+make test COVERAGE_COMMAND='coverage run --source=authtools --branch --parallel-mode'
	cd tests && coverage combine && coverage html

django-%.tar.gz: export TMP=$(shell mktemp)
django-%.tar.gz:
	wget "https://www.djangoproject.com/download/$(patsubst django-%.tar.gz,%,$@)/tarball/" -O "$${TMP}"
	echo "$(DJANGO_CHECKSUM) " "$${TMP}" | sha256sum -c
	mv "$${TMP}" "$@"

auth_tests: django-$(DJANGO_VERSION).tar.gz
	@-rm -r ${SITE_PACKAGES}/$@
	tar -xf $< --strip-components=2 -C "${SITE_PACKAGES}" "Django-$(DJANGO_VERSION)/tests/auth_tests"

docs:
	cd docs && $(MAKE) html

.PHONY: test test-builtin test-authtools test-customuser coverage auth_tests docs
