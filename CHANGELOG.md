# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2026-06-01

### Added

- Support for deleting jobs older than a given age via the new `Delete_Jobs` argument.

## [1.2.1] - 2026-05-07

### Fixed

- Corrected a wrong module reference that prevented `main` from running.

## [1.2.0] - 2026-04-29

### Changed

- Upgraded to OpenOrchestrator 3.*.
- Switched to `uv` for dependency management.
- Removed `if __name__ == "__main__"` blocks.

## [1.1.0] - 2024-06-04

### Changed

- Improved performance by replacing select-and-loop operations with bulk SQL
  `DELETE`/`UPDATE` queries for deleting logs and queue elements and for
  anonymizing queue references, data, and messages.

## [1.0.0] - 2024-03-21

### Added

- Initial release of the GDPR-Bot for deleting old data in an OpenOrchestrator
  database.
- Delete logs older than a given age (`Delete_Logs`).
- Delete queue elements older than a given age (`Delete_Queues`).
- Anonymize queue element references, data, and messages older than a given age
  (`Delete_Queue_References`, `Delete_Queue_Data`, `Delete_Queue_Messages`).

[1.3.0]: https://github.com/itk-dev-rpa/GDPR-Bot/releases/tag/1.3.0
[1.2.1]: https://github.com/itk-dev-rpa/GDPR-Bot/releases/tag/1.2.1
[1.2.0]: https://github.com/itk-dev-rpa/GDPR-Bot/releases/tag/1.2.0
[1.1.0]: https://github.com/itk-dev-rpa/GDPR-Bot/releases/tag/1.1.0
[1.0.0]: https://github.com/itk-dev-rpa/GDPR-Bot/releases/tag/1.0.0
