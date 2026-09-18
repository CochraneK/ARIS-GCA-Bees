# ARIS4C010 · Standalone Calibration Interface

A no-backend HTML generator is included as a platform-neutral fallback and QA interface.

## Properties

Each generated page:

- embeds exactly one verified participant form;
- shows one target-query trial at a time;
- supports P2 or P6 response buttons;
- records response time and confidence;
- hides researcher phenomenon tags and explicit retest markers;
- makes no network request;
- downloads a JSON response file locally at completion.

## Appropriate use

Useful for:

- laboratory/supervised pilot sessions;
- interface QA before moving to a survey/recruitment platform;
- local or institutionally hosted deployment;
- verifying that the study can be run independently of a commercial survey vendor.

## Not automatically sufficient for a remote study

At scale, a proper approved collection channel still needs:

- consent/participant information;
- secure response submission;
- session/completion management;
- compensation/recruitment workflow where applicable;
- institutional ethics/privacy requirements.

The generated HTML deliberately does not invent those organizational decisions.

## Privacy property

The standalone pages do not contain server submission code. Completion creates a local JSON file. A study administrator must define the approved method for collecting that file.
