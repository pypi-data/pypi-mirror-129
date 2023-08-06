# vi: set softtabstop=2 ts=2 sw=2 expandtab:
# pylint: disable=W0621
import os
import logging
from configparser import ConfigParser
from mergeconf import exceptions
from mergeconf.mergeconfsection import MergeConfSection

# deprecation apology message
deprecation_msg = """
This method is deprecated immediately.  I apologise for any inconvenience, but
I estimate uptake of this library to be in the low 1's and probably actually
just 1.  To continue using the API you're expecting, you can specify version
0.3 of the library but it was overhauled for better functionality and, I think,
a nicer API.
"""


class MergeConf(MergeConfSection):
  """
  Configuration class.  Initialized optionally with configuration items, then
  additional items may be added explicitly (and must be if they are mandatory,
  a specific type, etc.).  Once all items have been added the configuration is
  finalized with merge(), validation checks are performed, and the realized
  values can be extracted.

  This class inherits from the MergeConfSection class, which contains methods
  to define configuration items and sections and examine the configuration.
  """

  def __init__(self, codename, files=None, map=None, strict=True):
    """
    Initializes MergeConf class.

    Args:
      codename (str): Simple string which is assumed to prefix any related
        environment variables associated with the configuration (along with an
        underscore as separator), in order to avoid collisions in the
        environment's namespace.  For example, for an `app_name` configuration
        key, with a codename `MYAPP`, the corresponding environment variable
        would be `MYAPP_APP_NAME`.
      files (str or list): filename or list of filenames for configuration
        files.  Files are applied in order listed, and so should be listed from
        least to most important.
      map (dict): Configuration options which are neither mandatory nor of a
        specified type, specified as key, value pairs.
      strict (boolean): If true, unexpected configuration sections or items
        will cause an exception (`UndefinedSection` or `UndefinedConfiguration`,
        respectively).  If false, they will be added to the merged
        configuration.

    Note: The `map` argument is probably to be deprecated and removed at a
      later date.  Its utility is limited and should be avoided.
    """
    super().__init__(None, map=map)

    self._codename = codename
    self._strict = strict

    self._files = files
    if files and not isinstance(files, (list, tuple)):
      self._files = (files,)

    # main section name transparently added.  ConfigParser requires all items
    # to be contained in a section; this supports simpler configurations and
    # avoids having to create a "main" or "app" section explicitly if not
    # desired.
    self._main = '__app__'

    if map:
      logging.warning("Support for `map` argument is deprecated and will " \
        "be removed.  Please use `add()` to add configuration options and " \
        "their specifications, including default values.")

  def merge_environment(self):
    """
    Using configuration definition, reads in variables from the environment
    matching the pattern `<codename>[_<section_name>]_<variable_name>`.  Any
    variable found not matching a defined configuration item is returned in
    a list: in this way variables outside the merged configuration context can
    be handled, such as a variable specifying an alternative config file.

    Returns:
      Map of environment variables matching the application codename.  The
      keys will be stripped of the codename prefix and will be converted to
      lowercase.
    """
    # add this to any environment variable names
    prefix = self._codename.upper() + '_'

    # get all environment variables starting with that prefix into dict with
    # key stripped of prefix and made lowercase
    envvars = {
      # TODO(3.9): replace `split(prefix, 1)[1]` with `removeprefix(prefix)`
      x[0].split(prefix, 1)[1].lower(): x[1]
      for x in os.environ.items() if x[0].startswith(prefix)
    }

    self._merge_env(envvars)

    return envvars

  def merge_file(self, config_file):
    """
    Merge configuration defined in file.  File is expected to adhere to the
    format defined by ConfigParser, with `=` used as the delimiter and
    interpolation turned off.  In addition, unlike ConfigParser, config files
    may include variables defined prior to any section header.

    Arguments:
      config_file (str): Path to config file.
    """
    config = ConfigParser(delimiters='=', interpolation=None)

    # read configuration into string so we can prepend a pretend main section.
    # See definition of self._main for explanation.
    try:
      with open(config_file) as f:
        config_content = f"[{self._main}]\n{f.read()}"
    except FileNotFoundError:
      # pylint: disable=raise-missing-from
      raise exceptions.MissingConfigurationFile(config_file)

    # read configuration
    config.read_string(config_content, source=config_file)

    # read into stuffs
    for section in config.sections():
      if section == self._main:
        ref = self
      elif section not in self._sections:
        # unrecognized configuration section
        if self._strict:
          raise exceptions.UndefinedSection(section)
        logging.warning("Unexpected section in configuration: %s", section)
        ref = self.add_section(section)
      else:
        ref = self._sections[section]
      for option in config.options(section):
        if option not in ref._items:
          if self._strict:
            raise exceptions.UndefinedConfiguration(section, option)
          logging.warning("Unexpected configuration item in section %s: %s",
            section, option)
          ref.add(option, config[section][option])
        else:
          ref._items[option].value = config[section][option]

  def validate(self):
    """
    Checks that mandatory items have been defined in configuration.  If not,
    throws exception.  Client may also use `missing_mandatory()`.

    Subclasses may add additional validation but should first call the parent
    implementation as the test for mandatory items is primary.
    """
    # TODO(3.8): use walrus operator
    # if unfulfilled := self.missing_mandatory():
    unfulfilled = self.missing_mandatory()
    if unfulfilled:
      raise exceptions.MissingConfiguration(', '.join(unfulfilled))

  def merge(self):
    """
    Takes configuration definition and any configuration files specified and
    reads in configuration, overriding default values.  These are in turn
    overridden by corresponding variables found in the environment, if any.
    Basic validations are performed.

    This is a convenience method to handle the typical configuration
    hierarchy and process.  Clients may also call other `merge_*` methods in
    any order, but should call `validate()` if so to ensure all mandatory
    configurations are specified.
    """

    # get configuration file(s) from environment, fall back to default
    from_env = os.environ.get(f"{self._codename.upper()}_CONFIG")
    config_files = from_env.split(',') if from_env else self._files

    # if we have config files, merge into config
    if config_files:
      for config_file in config_files:
        logging.debug("Merging in config file %s", config_file)
        self.merge_file(config_file)

    # override with variables set in environment
    self.merge_environment()

    # test that mandatory values have been set
    self.validate()

  # -------------------------------------------------------------------------
  #                                                       deprecated methods
  # -------------------------------------------------------------------------

  # pylint: disable=no-self-use
  def add_boolean(self, key, value=None, mandatory=False):
    """
    _Deprecated._  Add a configuration item of type Boolean.

    Args:
      key (str): Name of configuration item
      value (boolean): Default value, None by default
      mandatory (boolean): Whether item is mandatory or not, defaults to
        False.

    Note: This is deprecated; simply use `add` with `type=bool`.
    """
    raise exceptions.Deprecated(version='0.3', message=deprecation_msg)

  # pylint: disable=no-self-use
  def parse(self, *args, **kwargs):
    """
    Deprecated.  See merge().
    """
    raise exceptions.Deprecated(version='0.3', message=deprecation_msg)
