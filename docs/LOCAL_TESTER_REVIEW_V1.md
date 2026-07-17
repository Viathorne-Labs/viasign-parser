# Local Tester Review V1

- **Status:** Website baseline credited; enabled tester human accessibility and repository-owner wording reviews complete; source publication approved; broader reviews pending
- **Recorded:** 2026-07-14
- **Human accessibility check:** 2026-07-17
- **Repository-owner wording review:** 2026-07-17
- **Source-publication approval:** 2026-07-17
- **Public parser base:** `aeca8bedadf16655fea34726bb3db9e780ba0f07`
- **Local parser candidate:** `0.2.1`
- **Website candidate:** `ae194e950783c58b2da0f59477b648262f44db91`
- **Human-check website:** `c6241de75ffc26c72735e0b761cd8840fec387b5`
- **Public activation:** Blocked

## Scope

This checkpoint covers a browser-assisted review of the enabled
`viathorne-web` tester against the public-parser candidate later approved for
source publication in parser PR #4. Both services ran only on loopback
addresses with an explicit local CORS origin. No Render preview, production API,
DNS, production CORS, public traffic, or visitor submission was used.

The review record contains no submitted sentence, reviewer identity, private
source, private fixture, or parser output copied from a private system. Test
inputs were independently authored and non-sensitive, and were cleared after
the checks.

The website candidate's `ACCESSIBILITY_AUDIT.md` already records the completed
representative `viathorne-web` accessibility baseline: human keyboard review,
native 200 percent zoom, Safari with VoiceOver, native macOS contrast settings,
reduced motion, forced colours, focus visibility, and route-wide structural
checks. Its recorded scope includes the shared ViaSign page and disabled tester
boundary. This checkpoint reuses that evidence instead of requesting a repeat
of the site-wide audit.

## Fail-closed safety correction

The review first found that the name-sign generation block recognized the
compound in one word order but not its reversed order. The repository owner then
selected a stricter public boundary: all recognized name-sign-related input is
unsupported, including informational, declarative, and generation wording.

The local candidate normalizes matching text with Unicode NFKC, recognizes
singular, plural, spaced, hyphenated, underscored, punctuation-separated, and
closed-compound `name sign` / `sign name` forms, and fails closed whenever a
name-related term and a sign/SgSL term occur anywhere in the same input. This
includes common inflections, possessives, and intervening words. The
conservative lexical rule may refuse an unrelated sentence containing both
terms; that is an intentional safety tradeoff, not a claim of perfect semantic
detection.

The blocked path returns `outcome=unsupported` with `analysis=null`. It does not
analyze, infer, generate, assign, or propose a name sign. Focused parser and API
tests use neutral synthetic inputs and confirm that submitted text is not
returned.

This is a safety-boundary correction, not an SgSL grammar rule, translation
feature, vocabulary addition, or motion capability.

## Browser-assisted evidence

| Check | Local result |
| --- | --- |
| Initial state | Input is empty, result region is hidden, and the status says the tester is ready. |
| Closed surface path | A neutral non-sensitive fixture returns visible uncertainty, human review required, motion unavailable, and no SgSL form or gloss. |
| Name-sign boundary | The locally reviewed reversed wording returned unsupported with no analysis; focused parser and API regressions now cover informational, declarative, plural, possessive, inflected, reversed, closed-compound, Unicode-separator, intervening-word, and explicit paraphrase variants. |
| Unavailable API path | The tester hides results and reports that the service is unavailable or unsafe without claiming the input was stored. |
| Contract boundary | The website accepts only schema `viasign.parser.response.v1`, contract `1.1.0`, safe outcomes, closed surface categories, and the required parser provenance. |
| Safety invariants | Accepted responses retain `review_required=true` and `motion_ready=false`; unsafe or incompatible responses fail closed. |
| Input echo | The website rejects a response containing the submitted text, and the API tests confirm no public response echo. |

## Accessibility evidence and limits

The local page exposes a labelled tester region, an explicitly labelled
textarea, help and character-count descriptions, a submit button, a polite
atomic status region, and a separately labelled result region. The result is
hidden before submission. The textarea has a visible three-pixel focus outline.

No horizontal page overflow was observed at 390-pixel and 640-pixel browser
widths. The textarea and submit button remained within the viewport. The input
retains the public 1,000-character limit.

The completed website baseline remains valid for the shared layout, navigation,
focus, motion, and representative page behavior. The enabled tester also passed
browser-assisted keyboard order, focus, and 390/640-pixel reflow checks. The
remaining work is not another site-wide audit.

On 2026-07-17, a bounded human accessibility pass reported that keyboard
navigation remained usable; a safe result stayed readable at native 200 percent
zoom and with increased system contrast; and Safari with VoiceOver read the
requested ready, checking, and final status phrases followed by the newly
revealed `Review details`, `Human review required`, and `Motion ready: No`
content. No clipping, overlap, unreadable state, or missing requested phrase was
reported.

This completes the enabled tester's bounded human accessibility delta. The
unavailable-state VoiceOver path was not part of this human pass and remains
covered only by browser-assisted behavior evidence. The repository-owner
wording decision is recorded below; broader Deaf/SgSL community review remains
separate and pending.

These checks were not present in the completed disabled-tester boundary. They
do not reopen the website's completed accessibility-hardening milestone or
establish linguistic correctness, community approval, or production readiness.

## Repository-owner enabled-flow wording review

On 2026-07-17, the repository owner approved five local wording boundaries:

1. Keep the tester described as local and not publicly enabled until a separate
   activation decision, then update the website, privacy notice, and
   documentation atomically.
2. Describe the current parser as limited natural-English surface analysis with
   visible uncertainty and motion unavailable, not SgSL grammar, translation,
   signing, or a tool for certified, legal, medical, safety-critical, or
   emergency communication.
3. State that the ViaSign application does not persist or echo submitted
   sentences, while disclosing that hosting providers may process technical
   network metadata; exact provider logging and retention still require live
   verification before activation. Sensitive-input and consent boundaries stay
   explicit.
4. Describe ViaSign as research toward future SgSL support, grounded in the
   founder's lived experience without claiming validated SgSL capability or
   broad Deaf-community endorsement.
5. State that Apache-2.0 permits use, modification, and redistribution of the
   public parser source and original repository documentation while keeping the
   ViaSign/Viathorne names, marks, website copy, branding, designs, private
   material, community knowledge, and personal data outside that grant.

This repository-owner wording decision is not broader Deaf/SgSL community
approval, security/privacy deployment approval, source-publication approval,
deployment approval, or public-activation approval.

## Separate source-publication decision

On 2026-07-17, after the independent final review, the repository owner
separately approved source publication and merge of parser PR #4. The reviewed
candidate was commit `f12b2b9b4b16e89e9a92a544da0a7101af5d5e2f`; the only
later candidate edits permitted by this decision are the mechanical
authorization record, its generated manifest hashes, and their focused tests.

This approval is source-publication-only. It does not authorize a Render update,
DNS change, production CORS, website API configuration, maintenance-mode
removal, deployment, public traffic, visitor submissions, or public activation.
Broader Deaf/SgSL community and security/privacy deployment reviews remain
pending.

No reviewer name, disability status, feedback content, or test sentence should
be added to the public record. A later public checkpoint may record only the
review scope, result, limitations, and approval state.

## Gate decision

This evidence and the later separate owner decision authorize source publication
and merge of parser PR #4 only. They do not authorize a Render update, DNS
change, production CORS, website API configuration, maintenance-mode removal,
deployment, public traffic, visitor submissions, or public activation.

Any missing review invariant, returned sentence text, SgSL overclaim, hidden
uncertainty, inaccessible state change, or analysis or proposal of recognized
name-sign-related input is a stop condition. Passing these checks demonstrates
structural consistency, not linguistic correctness or community approval.
