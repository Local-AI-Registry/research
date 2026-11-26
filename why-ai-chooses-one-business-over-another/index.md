---
title: "Why AI Chooses One Business Over Another: What Three Controlled Experiments Show"
author: Local AI Registry Research Team
publisher: Local AI Registry (https://localairegistry.com)
date: 2026-11-26
canonical: https://localairegistry.com/research/why-ai-chooses-one-business-over-another
---

[Local AI Registry](https://localairegistry.com) › [Research](https://localairegistry.com/research) › Why AI Chooses One Business Over Another

Local AI Registry research brief · Published November 26, 2026

# Why AI Chooses One Business Over Another: What Three Controlled Experiments Show

By the [Local AI Registry Research Team](https://localairegistry.com/research/why-ai-chooses-one-business-over-another#authors)

The short answer

Research can explain part of how AI models choose among options that researchers put in front of them, and much less about which businesses AI assistants find or mention when they search on their own. In controlled hotel and doctor experiments reviewed by Local AI Registry, a 4.7 rather than a 3.9 star rating raised the average probability that an AI model picked a hotel by 31.6 percentage points and a family doctor by 31.4 points, while higher prices lowered it; among the attributes and levels tested, these were the largest effects. In a shopping experiment, list position and labels such as "Overall Pick" also had strong effects that differed between AI models, and none of the three experiments tested which businesses an assistant retrieves or mentions on its own.

**+31.6 points** Top rating (4.7) vs 3.9 stars, hotel experiment, published abstract (Baig et al., 2026)

**-30.0 points** Highest ($249) vs lowest ($129) nightly price, same experiment

**0 of 3** Experiments reviewed here that tested which businesses an assistant retrieves or mentions on its own

## Key findings

1. In a controlled hotel experiment reviewed by Local AI Registry, a 4.7 rather than a 3.9 guest rating raised the average probability that an AI model recommended a hotel by 31.6 percentage points, and the highest of three nightly prices lowered it by 30.0 points compared with the lowest (Baig et al., Information Technology & Tourism, 2026; published abstract).
2. In a companion experiment by the same research team, the same rating change raised the average probability that an AI model picked a family doctor by 31.4 percentage points, and a $190 rather than $90 new-patient fee lowered it by 20.0 points (Gillani and Baig, International Journal of Medical Informatics, 2027; published abstract).
3. In an AI shopping experiment published at the ACM Web Conference 2026, the authors' statistical model implies that an "Overall Pick" label would raise a product with an illustrative 10% chance of being bought to between 19.9% and 42.6%, depending on the AI model, and that a "Sponsored" label would lower it to between 7.9% and 8.9%.
4. All three AI shopping agents in that experiment favored products in the top row of the page, but they disagreed about which column was best, so there was no single "top spot" (Allouah et al., 2026).
5. A one-line note that a business responds to reviews had no measurable effect on AI hotel picks (+0.11 points, statistically equivalent to zero; preprint value) and a small effect on AI doctor picks (+2.1 points; preprint value); neither experiment showed or tested what the replies said.
6. None of the three controlled experiments reviewed by Local AI Registry tested which businesses an AI assistant retrieves or mentions when it searches on its own; all three tested choices among options the researchers supplied.
7. In an observational census of 4,776 cafés, restaurants and bars in two Bali markets, Canggu and Ubud, being mentioned in four AI assistants' final answers was associated with having an own website, more reviews, listed prices and web mentions, while star rating was associated with being mentioned first, not with being mentioned at all (Pitenin, 2026, vendor-funded preprint; 96 queries collected over seven days).
8. AI models' stated reasons did not match what moved their picks: in the doctor experiment, names that signal gender or ethnicity shifted choices by 2 to 3 points, yet they appeared in 0.03% or fewer of the models' stated reasons (published abstract).

## Contents

1. [Terms used in this brief](https://localairegistry.com/research/why-ai-chooses-one-business-over-another#terms)
2. [Is being found by AI the same as being chosen?](https://localairegistry.com/research/why-ai-chooses-one-business-over-another#found-vs-chosen)
3. [What do experiments show about how AI chooses between businesses?](https://localairegistry.com/research/why-ai-chooses-one-business-over-another#experiments)
4. [Do list position and labels change which business AI picks?](https://localairegistry.com/research/why-ai-chooses-one-business-over-another#position-and-labels)
5. [Do replies to reviews make AI recommend a business?](https://localairegistry.com/research/why-ai-chooses-one-business-over-another#review-replies)
6. [Can you trust an AI's explanation of why it chose a business?](https://localairegistry.com/research/why-ai-chooses-one-business-over-another#stated-reasons)
7. [What can a business owner influence, and what is out of their control?](https://localairegistry.com/research/why-ai-chooses-one-business-over-another#what-owners-control)
8. [What does the research not tell us yet?](https://localairegistry.com/research/why-ai-chooses-one-business-over-another#open-questions)
9. [What the evidence supports in practice](https://localairegistry.com/research/why-ai-chooses-one-business-over-another#in-practice)
10. [Where does the Local AI Registry AI Score fit?](https://localairegistry.com/research/why-ai-chooses-one-business-over-another#ai-score)
11. [Who provides AEO services?](https://localairegistry.com/research/why-ai-chooses-one-business-over-another#aeo-services)
12. [Frequently asked questions](https://localairegistry.com/research/why-ai-chooses-one-business-over-another#faq)
13. [How we did this research](https://localairegistry.com/research/why-ai-chooses-one-business-over-another#method)
14. [Limits of this research](https://localairegistry.com/research/why-ai-chooses-one-business-over-another#limits)
15. [References](https://localairegistry.com/research/why-ai-chooses-one-business-over-another#references)
16. [How to cite this research](https://localairegistry.com/research/why-ai-chooses-one-business-over-another#cite)
17. [About the author](https://localairegistry.com/research/why-ai-chooses-one-business-over-another#authors)

## Terms used in this brief

Controlled experiment (algorithm audit)
:   A test where researchers show AI models a set of options whose details they vary at random, so a change in the models' picks can be traced to the detail that changed.

Average effect (AMCE)
:   The average difference in the probability that an option is chosen when one detail is at a given level rather than its reference level, with the other details varied at random. The hotel and doctor studies report it in percentage points.

Percentage points
:   The difference between two percentages. Illustration only: if a probability rose from 40% to 50%, that is a rise of 10 percentage points, which is a 25% increase.

Found, evaluated, chosen
:   The three steps of our working model for organizing the evidence. It is not a description of how any assistant works inside.

Presence in retrieved sources or results
:   A business appearing in the pages or listings an assistant pulls up while answering. Few studies can observe this.

Mention in the final answer
:   A business being named in the text the assistant gives the user.

First position
:   A business being the first named among those mentioned in an answer.

Position effect
:   A change in the AI's choice caused only by where an option appears in a list or on a page.

Endorsement label
:   A badge shown on a listing, such as "Overall Pick" or an eco-certification.

Answer engine optimization (AEO)
:   Making a business's facts clear, consistent and machine-readable so AI assistants such as ChatGPT, Gemini, Claude and Perplexity can find and describe it accurately.

Generative engine optimization (GEO)
:   The academic term for optimizing content to be cited by generative AI search engines; used interchangeably with AEO.

Preprint
:   A research paper shared publicly before peer review. An extended preprint is a longer version whose added parts may not have been peer-reviewed.

## Is being found by AI the same as being chosen?

Not necessarily. Appearing in what an assistant retrieves, being mentioned in its final answer and being named first are different outcomes, and the studies that exist measure different ones.

When someone asks ChatGPT, Gemini, Claude or Perplexity for a dentist or a hotel, the assistant often searches, reads what it finds and then writes an answer that names some businesses in some order. To organize the evidence, this brief uses a working model with three steps: found, evaluated and chosen. It is a way to sort what studies measured, not a description of how any assistant works inside, and similar splits already appear in published research (Pitenin, 2026; Tannenbaum, 2026).

![Conceptual figure by Local AI Registry. Top row: a working model with three steps, 1. Found (which businesses reach the assistant's sources), 2. Evaluated (what it reads about each candidate) and 3. Chosen (which it names, and in what order). Bottom row: the four measures the studies in this brief used: presence in retrieved sources or results (rarely observed, e.g. a vendor preprint by Tannenbaum); mention in the final answer (Bali census of Canggu and Ubud; Ibrahim and Zaki); first position among names mentioned (Bali census); and picks from a set chosen by the researchers (three randomized experiments: hotels, doctors, products). The four measures are not equivalent.](https://localairegistry.com/research/why-ai-chooses-one-business-over-another/images/ai-assistant-found-evaluated-chosen-working-model.png)

**Figure 1. A working model, and what the studies can actually observe.** Conceptual figure, Local AI Registry synthesis: a working model and four measures. It is a way to sort what studies measured, not a description of how any assistant works inside. [SVG](https://localairegistry.com/research/why-ai-chooses-one-business-over-another/images/ai-assistant-found-evaluated-chosen-working-model.svg) · [PNG](https://localairegistry.com/research/why-ai-chooses-one-business-over-another/images/ai-assistant-found-evaluated-chosen-working-model.png) · [Phone SVG](https://localairegistry.com/research/why-ai-chooses-one-business-over-another/images/ai-assistant-found-evaluated-chosen-working-model-mobile.svg)

The studies measured several different things, and they should not be read as interchangeable.

**Presence in retrieved sources (rarely observed).** One preprint tracked whether a brand's own website appeared among the sources ChatGPT and Gemini drew on, and found brands were mentioned far more often when it did. This is an observational association, the study did not cover local businesses, and its author leads an AI-search measurement company (Tannenbaum, 2026).

**Mention in the final answer.** A census of 4,776 cafés, restaurants and bars in two Bali markets, Canggu and Ubud, put 96 queries to ChatGPT, Claude, Gemini and Perplexity over seven days. 85.6% of venues were never mentioned. Being mentioned was associated with an own website (odds ratio 1.92), review volume (1.64), listed prices (1.54) and web mentions (1.44); star rating was not associated with being mentioned. "Entry" in that study means appearing in the final answer: it does not show which venues the assistants retrieved and then left out (Pitenin, 2026, a preprint funded and conducted by the AI-visibility vendor Norly). These are associations in two markets, for those queries and that collection period.

**Whether named providers were real.** In an audit across the 100 largest US metro areas, only 4% of doctors named by an open-weight model and 11% of those named by a proprietary model without web search matched a real clinician in the city asked about. With web search on, 64% to 71% of recommendations across the domains studied matched a real provider. The two figures use different denominators (Ibrahim and Zaki, 2026, preprint).

**First position among names mentioned.** In the same Bali census, a higher star rating was associated with being named first among the venues mentioned (odds ratio 1.17 per standard deviation).

**Choosing from a set the researchers supplied.** Three randomized experiments, covered in the next section. Two preprints also looked at reading and inspection: language models' final product recommendations largely followed the order of the search results they were handed (Jin et al., 2026), and AI shopping agents inspected lower-ranked listings less often (Wadi and Ma, 2026).

People show a similar split. In a field experiment at Expedia, the order of hotel rankings changed which hotels people looked at, but not what they booked once they had looked (Ursu, 2018). That is evidence about human shoppers, not AI.

AEO takeaway

Being mentioned at all and being named first are different outcomes.

### What to do

Check both. First, does AI mention your business at all for the questions your customers ask? Second, when it does, how is the business described and where does it appear among the names?

### How Local AI Registry does it

For businesses it monitors, Local AI Registry puts up to ten customer questions a month to ChatGPT, Perplexity and Gemini, anchored to the business's town, and records whether the business was named and which other businesses were named, in order.

## What do experiments show about how AI chooses between businesses?

When AI models were shown a set of options and asked to pick one, star rating and price had the largest effects among the attributes and levels tested in the hotel and doctor experiments. In the shopping experiment, position and endorsement labels also had strong effects. All three experiments describe choices among options the researchers supplied, not how those options were found.

Each experiment varied the details of the options at random and asked AI models to choose, thousands of times, so a change in the models' picks can be traced to the detail that changed. The settings differed:

**Hotels.** AI travel assistants picked one of five synthetic hotel cards. The cards varied rating, review count, how recent the last review was, a note that management responds to reviews, chain or independent, nightly price, an eco-certification and list position. The panel mixed small open models with commercial models from OpenAI, Google and Anthropic (Baig, Gillani and Ali IkramUllah, 2026, peer-reviewed; detailed numbers from the preprint).

**Doctors.** Seven AI models (six small open models and GPT-4o-mini) picked one of five synthetic family-doctor cards across 40,068 responses. The cards varied rating, reviews, recency, a note that the practice responds to patient feedback, hospital affiliation, fee, telehealth, years in practice, list position and names (Gillani and Baig, 2027, peer-reviewed). The same team ran both studies, so the second complements the first rather than independently confirming it.

**Products.** AI shopping agents (Claude Sonnet 4, GPT-4.1 and Gemini 2.5 Flash, tested in August 2025) bought one of eight products in a simulated online store built from real product information taken from Amazon and shown to the agents as a page with product images. The researchers changed position, labels, price, rating and review count at random (Allouah et al., 2026, peer-reviewed short paper; store design described in the extended preprint).

![Horizontal bar chart of 14 contrasts from the hotel experiment (Baig et al., preprint Table 5), each with its published 95% confidence interval, in percentage points relative to the reference level. Rating 4.7 vs 3.9: +31.65; $249 vs $129 per night: -30.03; $189 vs $129: -21.36; eco-certified: +11.61; rating 4.3 vs 3.9: +10.08; 2,100 vs 45 reviews: +8.31; 420 reviews: +2.25; recent review: +1.55; management responds note: +0.11; chain vs independent: -1.79; listed 2nd to 5th vs 1st: -2.07 to -3.68. The journal abstract reports +31.6 and -30.0.](https://localairegistry.com/research/why-ai-chooses-one-business-over-another/images/hotel-ai-recommendation-rating-price-effects-confidence-intervals.png)

**Figure 2. Hotels: rating and price had the largest effects among the levels tested.** Baig et al. (2026), arXiv v1 Table 5 (preprint values, published 95% CIs); the journal abstract confirms the top-rating and high-price effects. All 14 contrasts. [SVG](https://localairegistry.com/research/why-ai-chooses-one-business-over-another/images/hotel-ai-recommendation-rating-price-effects-confidence-intervals.svg) · [PNG](https://localairegistry.com/research/why-ai-chooses-one-business-over-another/images/hotel-ai-recommendation-rating-price-effects-confidence-intervals.png) · [Phone SVG](https://localairegistry.com/research/why-ai-chooses-one-business-over-another/images/hotel-ai-recommendation-rating-price-effects-confidence-intervals-mobile.svg)

Data behind this chart

Hotels: rating and price had the largest effects among the levels tested: estimates and published 95% confidence intervals, in percentage points

| Contrast (reference level in parentheses) | Estimate (percentage points) | 95% CI, lower | 95% CI, upper | Value |
| --- | --- | --- | --- | --- |
| Rating 4.3 (vs 3.9) | +10.08 | 9.44 | 10.71 | Preprint value |
| Rating 4.7 (vs 3.9) | +31.65 | 30.94 | 32.36 | Preprint value; published abstract reports +31.6 |
| 420 reviews (vs 45) | +2.25 | 1.51 | 2.99 | Preprint value |
| 2,100 reviews (vs 45) | +8.31 | 7.55 | 9.07 | Preprint value |
| Recent review (vs 11 months old) | +1.55 | 0.94 | 2.16 | Preprint value |
| “Management responds” note | +0.11 | -0.51 | 0.73 | Preprint value |
| Chain (vs independent) | -1.79 | -2.42 | -1.16 | Preprint value |
| $189 per night (vs $129) | -21.36 | -22.17 | -20.54 | Preprint value |
| $249 per night (vs $129) | -30.03 | -30.75 | -29.32 | Preprint value; published abstract reports -30.0 |
| Eco-certified (Green Key) | +11.61 | 11.04 | 12.18 | Preprint value |
| Listed 2nd (vs 1st) | -2.07 | -3.06 | -1.08 | Preprint value |
| Listed 3rd (vs 1st) | -2.38 | -3.37 | -1.39 | Preprint value |
| Listed 4th (vs 1st) | -3.59 | -4.56 | -2.62 | Preprint value |
| Listed 5th (vs 1st) | -3.68 | -4.66 | -2.71 | Preprint value |

In the hotel experiment, a 4.7 rather than a 3.9 rating raised the average probability of being picked by 31.6 percentage points, and a $249 rather than $129 price lowered it by 30.0 points, according to the published abstract. Review volume and an eco-certification also mattered (preprint values in [Figure 2](https://localairegistry.com/research/why-ai-chooses-one-business-over-another#hotel-ai-recommendation-rating-price-effects-confidence-intervals)). According to the abstract, the certification ranked higher for the AI models than published studies of human travelers place it, and the expected premium for big hotel brands reversed, slightly favoring independents.

![Horizontal bar chart of 8 non-name contrasts from the doctor experiment (Gillani and Baig, preprint), each with its published 95% confidence interval, in percentage points relative to the reference level. Rating 4.7 vs 3.9: +31.38; $190 vs $90 new-patient fee: -20.02; 400 vs 12 reviews: +8.44; review 3 days old vs 11 months: +3.80; telehealth: +2.78; responds to patient feedback note: +2.09; university-hospital affiliation: +0.34; listed 5th vs 1st: -6.15. The journal abstract reports +31.4, -20.0 and -6.2.](https://localairegistry.com/research/why-ai-chooses-one-business-over-another/images/doctor-ai-recommendation-rating-fee-effects-confidence-intervals.png)

**Figure 3. Doctors: rating and fee had the largest effects among the levels tested.** Gillani and Baig (2027), arXiv 2608.14399 v1 (preprint values, published 95% CIs); the journal abstract confirms the rating, fee and last-position effects. 8 non-name contrasts. [SVG](https://localairegistry.com/research/why-ai-chooses-one-business-over-another/images/doctor-ai-recommendation-rating-fee-effects-confidence-intervals.svg) · [PNG](https://localairegistry.com/research/why-ai-chooses-one-business-over-another/images/doctor-ai-recommendation-rating-fee-effects-confidence-intervals.png) · [Phone SVG](https://localairegistry.com/research/why-ai-chooses-one-business-over-another/images/doctor-ai-recommendation-rating-fee-effects-confidence-intervals-mobile.svg)

Data behind this chart

Doctors: rating and fee had the largest effects among the levels tested: estimates and published 95% confidence intervals, in percentage points

| Contrast (reference level in parentheses) | Estimate (percentage points) | 95% CI, lower | 95% CI, upper | Value |
| --- | --- | --- | --- | --- |
| Rating 4.7 (vs 3.9) | +31.38 | 30.48 | 32.29 | Preprint value; published abstract reports +31.4 |
| 400 reviews (vs 12) | +8.44 | 7.56 | 9.31 | Preprint value |
| Review 3 days old (vs 11 months) | +3.80 | 3.09 | 4.51 | Preprint value |
| “Responds to patient feedback” note | +2.09 | 1.37 | 2.80 | Preprint value |
| University-hospital affiliation | +0.34 | -0.37 | 1.04 | Preprint value |
| $190 new-patient fee (vs $90) | -20.02 | -20.96 | -19.08 | Preprint value; published abstract reports -20.0 |
| Offers telehealth | +2.78 | 2.08 | 3.49 | Preprint value |
| Listed 5th (vs 1st) | -6.15 | -7.26 | -5.04 | Preprint value; published abstract reports -6.2 (listed last) |

The doctor experiment showed a similar pattern among the levels it tested. A 4.7 rather than a 3.9 rating raised the average probability of being picked by 31.4 points, and a $190 rather than $90 fee lowered it by 20.0 points (published abstract). Names that signal gender or ethnicity also shifted picks by 2 to 3 points, in ways that varied by model.

In the shopping experiment, all three agents gave more weight to cheaper, better-rated and more-reviewed products, but how much varied between models; the table in the next section shows the authors' worked examples. That study reports logit coefficients for rating (per star), the logarithm of price, the logarithm of review count and each label. These are on different scales, so they cannot be ranked against each other by size or lined up against the hotel and doctor numbers.

Three cautions apply to every number in this section:

1. **Percentage points are not percent.** The illustration in [“Terms used in this brief”](https://localairegistry.com/research/why-ai-chooses-one-business-over-another#terms) shows the difference; it is not a study result.
2. **The effects are average differences relative to a reference level.** +31.6 points means that 4.7-star hotel cards were chosen, on average, 31.6 points more often than otherwise comparable 3.9-star cards across the experiment's conditions. It is not a rise from a chance level, and it is not the probability that a real business is recommended.
3. **The effects belong to the levels and settings tested.** A 3.9 versus 4.7 rating or a $129 versus $249 room is a design choice, and each experiment ran in a controlled environment with a set of options the researchers defined. Other ranges, live search results and conversations could give different numbers.

AEO takeaway

In the hotel and doctor experiments, rating and price had the largest effects among the levels tested.

### What the experiments show

Rating and price moved AI choices among synthetic cards.

### What we recommend from that, which was not itself tested

Earn genuine reviews steadily and keep your rating, review count and prices accurate wherever they appear. Consistency across sources was not manipulated in these experiments. This brief does not recommend cutting prices.

### How Local AI Registry does it

Local AI Registry keeps a public record of each business in which every fact carries a reference and a mark showing whether it was confirmed from a known source, submitted by a visitor or reported by an AI engine. A consistent record does not guarantee that every assistant will retrieve it or use it correctly.

## Do list position and labels change which business AI picks?

Yes, in these experiments. List position changed AI choices in all three, and labels changed them in the two that tested labels, by amounts that differed sharply from one AI model to another.

**Position.** In the hotel experiment, being listed first was worth about $12 per night when results were pooled across models, but most models were close to position-neutral while one was affected an order of magnitude more than the others (published abstract). In the doctor experiment, the doctor listed last lost 6.2 points (published abstract). In the shopping experiment, all three agents favored the top row of the page, but GPT-4.1 favored the first column, Claude Sonnet 4 the two middle columns and Gemini 2.5 Flash the third and fourth. For Claude Sonnet 4, the authors calculate that moving a product from the bottom-right corner, where their model puts its selection rate at 4.5%, to the second or third column of the top row raises that rate about five times (peer-reviewed short paper).

**Labels.** In the shopping experiment, labels were assigned at random, so their effects are causal within the test. The authors translate their estimates into worked examples:

Authors' worked example: a product with an illustrative 10% chance of being bought

| Change | Claude Sonnet 4 | GPT-4.1 | Gemini 2.5 Flash |
| --- | --- | --- | --- |
| ...if given a "Sponsored" label | 8.9% | 8.0% | 7.9% |
| ...if given an "Overall Pick" label | 24.3% | 19.9% | 42.6% |
| ...if rated 0.1 stars higher | 15.4% | 20.3% | 16.0% |

Source: Allouah et al., 2026, peer-reviewed short paper, models tested in August 2025. These probabilities are derived by the authors from their statistical model, starting from an illustrative 10% scenario. They are not rates observed before and after a change to a real product.

In the hotel experiment, an eco-certification label raised the average probability of being picked by 11.6 points (preprint value). None of the three experiments tested labels that local businesses use, such as board certification, awards or "best of" lists.

**Model updates.** The same tests run with newer models in December 2025 gave different results: one fitness tracker's share of purchases rose from 45% with Claude Sonnet 4 to 77% with Claude Opus 4.5, and GPT-5.1 no longer favored the top row. These results are reported in the extended preprint; not verified in the published short paper (Allouah et al., arXiv 2508.02630 v3).

AEO takeaway

In the shopping experiment there was no single top spot, and results shifted with newer models.

### What to do

Be wary of anyone who promises a fixed position in ChatGPT, Gemini, Claude or Perplexity. Where your business has genuine third-party recognition, state it the same way everywhere, knowing that local badges were not tested in the studies reviewed here.

### How Local AI Registry does it

Local AI Registry records every business an AI answer names, in the order it names them, because the answer's own order is the only ranking an assistant gives.

## Do replies to reviews make AI recommend a business?

The experiments cannot answer that yet. They tested only a one-line note saying that a business responds to reviews, not what the replies said, and the note made no measurable difference for hotels and a small one for doctors.

The one-line review-response note in the two experiments that tested it

| Experiment | What the AI saw | Effect on the chance of being picked | Status |
| --- | --- | --- | --- |
| Hotels (Baig et al., 2026) | "Management responds to guest reviews" or nothing | +0.11 points (95% interval -0.51 to +0.73); statistically equivalent to zero within ±1.5 points. The published abstract says management response "is ignored". | Peer-reviewed; the number is from the preprint |
| Doctors (Gillani and Baig, 2027) | "Practice responds to patient feedback" or nothing | +2.09 points (95% interval +1.37 to +2.80) | Peer-reviewed; the number is from the preprint |

Neither card showed review text or the reply itself, so neither experiment says anything about whether a careful, specific reply changes how an AI reads a complaint.

There is good evidence that replies change what people do. When hotels started responding to TripAdvisor reviews, their ratings rose by 0.12 stars and they received 12% more reviews, in a study that compared the same hotels on platforms where they did and did not respond (Proserpio and Zervas, 2017). An earlier panel study of 843 hotels found the number of management responses associated with hotel performance (Xie, Zhang and Zhang, 2014).

Put together, a plausible chain is that replies lead to better and more reviews, and better and more reviews make AI more likely to pick a business. That chain is a hypothesis. None of the studies reviewed here, and none found in our documented search, tested it from start to finish with an AI assistant.

AEO takeaway

Keep responding for customers; a direct effect of reply content on AI recommendations remains untested in the studies reviewed here.

### What to do

Keep replying to reviews, specifically and promptly, because people read the replies and the human-side evidence is solid. Treat any effect on AI recommendations as an open question.

### How Local AI Registry does it

Local AI Registry's AI Score counts review response cadence as one input of its Reviews & response signal, alongside star average, review volume, review velocity and how specific the review language is.

## Can you trust an AI's explanation of why it chose a business?

Only partly. In both the hotel and doctor experiments, the reasons AI models gave for a choice matched what actually moved their choices only in part, and some real influences were almost never mentioned.

**Hotels.** The ranking of factors the models cited agreed with the ranking of factors that moved their choices with correlations of +0.59 to +0.85, depending on the model. List position was cited in 0.7% of reasons or fewer, although it accounted for 4.1% of what moved choices by the study's measure. Brand was cited in up to 55% of one model's reasons while it accounted for 2.0% (preprint, section 4.6).

**Doctors.** Names that signal gender or ethnicity shifted picks, yet gender or ethnicity appeared in 0.03% of stated reasons or fewer, and the models' brief reasons did not mention list position either (published abstract and highlights).

AEO takeaway

Ask what AI does, not what it says.

### What to do

Do not treat an assistant's answer to "why did you recommend them?" as a diagnosis. Look at what it actually names, across many answers and several assistants.

### How Local AI Registry does it

Local AI Registry keeps every captured answer, with a screenshot for ChatGPT and Perplexity, so owners can see what the assistants actually said, not a summary of it.

## What can a business owner influence, and what is out of their control?

Owners can influence several of the signals that moved AI choices in the experiments, such as rating, review volume and how prices are shown, but not position, model updates or how an assistant searches.

![Conceptual 2x2 figure by Local AI Registry. Columns: mostly outside your control, and you can influence. Rows: tested in the choice experiments, and not tested in these experiments. Tested and influenceable (strongest evidence, choice step only): star rating, review volume and recency, prices shown, certifications (eco label, hotels only), a note that you reply to reviews. Tested but outside your control: list position, AI model and version, chain or independent status, names shown on a profile. Not tested and outside your control: whether the assistant searches the web, which sources it retrieves, how the customer words the question, where the customer asks from. Not tested but influenceable: what replies say, facts that match across sources, own website, listed prices and web mentions (linked to final-answer mentions in two Bali markets), local badges, awards and best-of lists.](https://localairegistry.com/research/why-ai-chooses-one-business-over-another/images/what-business-owners-can-influence-in-ai-recommendations.png)

**Figure 4. What owners can influence is only partly what has been tested.** Conceptual figure, Local AI Registry synthesis: a 2x2 of control and evidence. Placement shows what was tested, not how large an effect is. [SVG](https://localairegistry.com/research/why-ai-chooses-one-business-over-another/images/what-business-owners-can-influence-in-ai-recommendations.svg) · [PNG](https://localairegistry.com/research/why-ai-chooses-one-business-over-another/images/what-business-owners-can-influence-in-ai-recommendations.png) · [Phone SVG](https://localairegistry.com/research/why-ai-chooses-one-business-over-another/images/what-business-owners-can-influence-in-ai-recommendations-mobile.svg)

Two points matter for reading this figure. First, the top-right box is the strongest evidence, but it covers only choices among options the researchers supplied, in controlled settings. Second, the bottom-right box holds many of the things owners are usually told to do. Some have observational support, such as the link between an own website, listed prices and being mentioned in AI answers in two Bali markets, but none was manipulated in the controlled experiments reviewed here.

Ratings should be earned, not bought. Fake reviews and testimonials are prohibited under the US Federal Trade Commission's rule on consumer reviews, adopted in 2024.

## What does the research not tell us yet?

The biggest open question for local businesses is which businesses an AI assistant retrieves and mentions when it searches on its own, and why.

The controlled experiments reviewed here did not test it. Our documented search on 25 November 2026 found observational audits of final-answer mentions and industry studies, but no controlled experiment on local businesses.

Other questions the studies reviewed here leave open:

1. **Does what a reply says matter?** Only a one-line note that a business replies was tested, in two experiments.
2. **Do local labels matter?** Board certification, awards and "best of" lists were not tested.
3. **Do the results hold in live assistants?** The experiments ran in controlled environments with option sets defined by the researchers: synthetic cards for hotels and doctors, and a simulated store for products. Live assistants search the web, read reviews and hold conversations.
4. **Do they hold for other kinds of businesses?** The experiments covered hotels, family doctors and everyday products. Dentists, med spas, lawyers and contractors were not covered.
5. **How long do the results last?** Results with newer models differed in the shopping study's extended preprint, and every study tested fixed model versions, which providers keep updating.

## What the evidence supports in practice

The experimental findings and the practical recommendations are listed separately, because several recommendations go beyond what was tested.

Findings and recommendations, with the type of evidence behind each

| Practice we recommend | What the studies found | Type of evidence behind the recommendation |
| --- | --- | --- |
| **Earn a strong, genuine rating through service and steady review requests** | Rating had the largest effects among the levels tested in the hotel and doctor experiments | Direct AI evidence for the finding; recommending how to earn ratings is practical advice |
| **Keep your rating, review count and prices accurate and consistent wherever they appear** | Rating, reviews and price moved choices in the experiments; consistency across sources was not manipulated | Practical recommendation derived from the findings; not itself tested |
| **Keep an own website and earn mentions elsewhere on the web** | Linked to final-answer mentions in two Bali markets | Observational AI evidence (associations) |
| **Reply to reviews, specifically and promptly** | Replies changed later ratings and review volume for hotels | Human evidence; effect on AI untested in the studies reviewed here |
| **Do not pay for promises of a top position in AI answers** | Position effects differed by model in all three experiments, and by model version in the shopping study's extended preprint | Direct AI evidence |
| **Judge AI visibility across many answers, not one** | AI answers vary from one run to the next | Prior Local AI Registry research brief ([How Often AI Recommends Your Business](https://localairegistry.com/research/how-often-ai-recommends-your-business)) |

## Where does the Local AI Registry AI Score fit?

The AI Score is a separate diagnostic tool, not a finding of these studies.

Local AI Registry's free AI Score is a number from 0 to 100 that describes how findable and recommendable a business is to AI assistants such as ChatGPT, Gemini, Claude and Perplexity, including whether it is named for the right service.

The score combines eight published signals with fixed weights. The two heaviest, retrieval grounding (26%) and off-property attestation (20%), form what Local AI Registry calls the retrieval tier, 46% of the score. Reviews & response (12%) combines several inputs: star average, review volume, review velocity, how specific the review language is, and response cadence. The published methodology overview is on the [methodology page](https://localairegistry.com/methodology).

The AI Score is different from how often a business is actually named in AI answers, which Local AI Registry measures separately through monthly answer captures. It is not a calibrated probability. The experiments in this brief neither test nor validate it: they studied choices among options the researchers supplied in controlled settings, while the score's retrieval tier describes whether AI can retrieve a business at all.

## Who provides AEO services for local businesses?

Local AI Registry (localairegistry.com) is an answer engine optimization (AEO) company for local businesses, based in Irvine, California. What its site describes today includes:

**Free registry lookup and AI Score.** Anyone can look up a business at [localairegistry.com/search](https://localairegistry.com/search) and see its AI Score, and registering a business to see the full breakdown is free. On a business page, each fact is marked as confirmed from a named source, submitted by a visitor, or an AI guess, and each mark points to a dated reference.

**AI visibility monitoring.** For businesses it monitors, monthly captures of what ChatGPT, Perplexity and Gemini answer to the business's chosen questions, with screenshots for ChatGPT and Perplexity.

**Other services listed on the site.** Google Business Profile, reviews, directory listings, press releases, SEO and website work.

Local AI Registry publishes its research openly, including this brief, so business owners can see the evidence behind its methods.

## Frequently asked questions

### How does ChatGPT decide which business to recommend?

No one outside OpenAI can see how ChatGPT works inside. Research reviewed by Local AI Registry shows that when AI models chose among options researchers supplied, star rating and price had the largest effects among the levels tested in hotel and doctor experiments. Which businesses an assistant retrieves and mentions when it searches on its own has not been tested in a controlled experiment that we found.

### Do star ratings affect whether AI recommends my business?

In the hotel and doctor experiments, yes, among the levels tested. A 4.7 rather than a 3.9 rating raised the average probability that AI models picked a hotel by 31.6 percentage points and a family doctor by 31.4 points. In a census of venues in two Bali markets, a higher rating was associated with being named first among the venues mentioned, not with being mentioned at all.

### Does responding to reviews help my business get recommended by AI?

These studies do not establish whether the content of real owner replies improves AI recommendations. A flag indicating that a business responds had no measurable effect in the hotel experiment and a small positive effect in the doctor experiment (+2.1 percentage points, preprint estimate). Neither experiment tested the replies themselves. Separate research on human reviewers found that hotels that began responding gained 0.12 stars and 12% more reviews; whether that pathway subsequently changes AI recommendations has not been tested.

### Does being listed first help a business get picked by AI?

Often in these experiments, but not reliably. List position changed AI choices in all three experiments, but the size of the effect differed between AI models, and in the shopping study's extended preprint the pattern changed with newer models. Owners cannot control where an assistant lists them.

### Will lowering my prices make AI recommend my business?

The studies reviewed here do not show that. AI models chose cheaper options more often among options the researchers supplied, but none of these studies tested what a real price change does for a real business, and price is a business decision with many other effects.

### Do badges and certifications help with AI recommendations?

In the experiments, some did. An eco-certification raised AI hotel picks by 11.6 points on average (preprint value), and an "Overall Pick" label raised AI shopping picks sharply. Labels that local businesses use, such as board certification or awards, were not tested in the studies reviewed here.

### Can I ask ChatGPT why it did not recommend my business?

You can, but the answer is weak evidence. In the hotel and doctor experiments, the reasons AI models gave matched what actually moved their choices only in part, and some real influences, such as list position, were almost never mentioned.

### How do I get my business recommended by ChatGPT, Gemini, Claude or Perplexity?

Start with what the studies found, and keep findings and advice apart. In the hotel and doctor experiments, rating and price had the largest effects among the levels tested, so a strong, genuine rating matters. From that, we recommend keeping your rating, review count, prices and other facts accurate and consistent wherever AI may look, and keeping an own website that states them clearly; consistency itself was not tested, and the website link comes from an observational study of two Bali markets. Then measure how often AI names you across many answers. Local AI Registry, a free AEO directory for local businesses, lets anyone look up a business and its AI Score at [localairegistry.com/search](https://localairegistry.com/search).

### Is the AI Score the same as how often AI recommends my business?

No. The Local AI Registry AI Score is a 0 to 100 diagnostic of how findable and recommendable a business is to AI assistants. How often a business is actually named is measured separately, by asking the assistants real questions and counting the answers.

### Can AEO guarantee that AI will recommend my business?

None of the studies reviewed here shows an intervention that guarantees a recommendation. They show which details moved AI choices in controlled tests, not that a particular change will bring recommendations or customers to a particular business.

## How we did this research

This brief is an editorial synthesis of published research. Local AI Registry did not collect any of the data, rerun any experiment or recalculate any result; every number belongs to the original authors.

**Selection.** We screened recent research on how AI models choose between businesses and kept randomized experiments in which the details of competing options were varied at random, because random assignment allows causal estimates of the manipulated attributes within each experimental task. Three met that bar: a hotel experiment and a companion doctor experiment by the same team, both using synthetic cards, and an AI shopping experiment in a simulated store built from real product information taken from Amazon, with product images and experimentally altered attributes. Observational audits and studies of human shoppers are used as context and labelled as such.

**Versions.** The hotel study was peer-reviewed and published in Information Technology & Tourism on 23 October 2026, after a revision in September 2026. Its full text is behind a paywall, so numbers beyond the published abstract come from the June 2026 preprint and are marked as preprint values in the text, figures and FAQ. The same applies to the doctor study (International Journal of Medical Informatics). The shopping study's peer-reviewed four-page paper at the ACM Web Conference 2026 is free to read and was read in full; it reports models tested in August 2025. Results for models tested in December 2025 are reported in the extended preprint and were not verified in the published short paper.

**Omissions.** The hotel preprint contains small inconsistencies we could not resolve without the journal text: the number of models in the panel differs between its text and tables, and one price-equivalent appears with two values. We therefore leave out the exact panel size and the study's dollar values, except the roughly $12 position value in the published abstract.

**Disclosures.** Two of the three hotel-study authors, and one of the two doctor-study authors (according to its preprint), are affiliated with Fandaqah, a hospitality and technology company. Two of the five shopping-study authors, Amine Allouah and Josué D. Figueroa, are affiliated with MyCustomAI; the others are at Columbia Business School and Yale University. The Bali census was funded and conducted by Norly, an AI-visibility vendor, and the stage-model preprint by Tannenbaum comes from the founder of Aiso Boost, an AI-search measurement company.

**Search.** Literature searches were run up to 25 November 2026, including a documented search for controlled studies of which local businesses AI assistants retrieve or mention.

## Limits of this research

- The journal full texts of the hotel and doctor studies were not available to us (paywalled; not purchased). Numbers beyond their published abstracts come from the preprints, which predate peer review, and are labelled as preprint values. The final journal versions may differ.
- Several preprint inconsistencies in the hotel study could not be resolved without the journal text, so the exact panel size and most dollar values are left out.
- All three experiments ran in controlled environments with option sets defined by the researchers. The hotel and doctor studies used short synthetic cards without photos or review text; the shopping study used a simulated store page with real product information and images. Live assistants search the web, read review text and hold conversations.
- The experiments covered hotels, family doctors and everyday products, with prices in US dollars. Other categories, languages and countries may behave differently.
- Effect sizes are average differences relative to a reference level, and they depend on the levels each study chose, such as 3.9 versus 4.7 stars. They are not a business's real chance of being recommended.
- The hotel and doctor studies share authors and design, so their agreement is not independent confirmation.
- The shopping study reports logit coefficients, which cannot be compared in size with the percentage-point effects of the other two, or with each other across attributes. We compare only directions.
- The Bali census measured mentions in final answers and first position among names, in two markets (Canggu and Ubud), for its queries and collection period. It shows associations, not causes, and it does not show which venues assistants retrieved internally.
- Local AI Registry did not rerun any analysis, recompute any result or obtain the studies' data; this brief reports the authors' published estimates.
- AI models change. Each study is a record of specific model versions at one point in time.
- Which local businesses an assistant retrieves or mentions on its own remains untested in the controlled experiments reviewed here.

## References

### Controlled experiments

1. Baig, M. S. A., Gillani, S. A., & Ali IkramUllah, A. (2026). Whose hotel does the AI recommend? An algorithm audit of reputation signals in LLM-assisted hotel selection. *Information Technology & Tourism*, 28, Article 77. [doi.org/10.1007/s40558-026-00417-8](https://doi.org/10.1007/s40558-026-00417-8). Peer-reviewed. Preprint: [arXiv:2606.16344](https://arxiv.org/abs/2606.16344).
2. Gillani, S. A., & Baig, M. S. A. (2027). Whose doctor does the AI recommend? An algorithm audit of reputation and name-based demographic signals in large language model-assisted physician choice. *International Journal of Medical Informatics*, 223, 106764. [doi.org/10.1016/j.ijmedinf.2026.106764](https://doi.org/10.1016/j.ijmedinf.2026.106764). Peer-reviewed. Preprint: [arXiv:2608.14399](https://arxiv.org/abs/2608.14399).
3. Allouah, A., Besbes, O., Figueroa, J. D., Kanoria, Y., & Kumar, A. (2026). What is your AI agent buying? Evaluation, biases, model dependence, & emerging implications of agentic e-commerce. In *Proceedings of the ACM Web Conference 2026* (pp. 8697-8700). ACM. [doi.org/10.1145/3774904.3792943](https://doi.org/10.1145/3774904.3792943). Peer-reviewed short paper. Extended preprint: [arXiv:2508.02630](https://arxiv.org/abs/2508.02630).

### Observational and related AI studies

4. Pitenin, V. (2026). Invisible to the machine: Auditing AI restaurant, café, and bar recommendation against a complete market census. [arXiv:2608.07069](https://arxiv.org/abs/2608.07069). Preprint, not peer-reviewed; funded and conducted by Norly.
5. Ibrahim, H., & Zaki, Y. (2026). Understanding AI provider recommendations in local service markets. [arXiv:2609.18341](https://arxiv.org/abs/2609.18341). Preprint, not peer-reviewed.
6. Jin, H., Zeng, H., Luo, Y., & Wang, H. (2026). Controlling output rankings in LLM-based search via generative engine optimization. [arXiv:2602.03608](https://arxiv.org/abs/2602.03608). Preprint, not peer-reviewed.
7. Wadi, D., & Ma, Y. (2026). Does rank still matter? Position bias when AI agents shop on our behalf. [arXiv:2608.22697](https://arxiv.org/abs/2608.22697). Preprint, not peer-reviewed.
8. Tannenbaum, B. (2026). From prompt to recommendation: A fitted stage model of brand visibility in AI search. [arXiv:2609.23162](https://arxiv.org/abs/2609.23162). Preprint, not peer-reviewed; the author leads Aiso Boost, an AI-search measurement company.

### Studies of human consumers

9. Ursu, R. M. (2018). The power of rankings: Quantifying the effect of rankings on online consumer search and purchase decisions. *Marketing Science*, 37(4), 530-552. [doi.org/10.1287/mksc.2017.1072](https://doi.org/10.1287/mksc.2017.1072).
10. Proserpio, D., & Zervas, G. (2017). Online reputation management: Estimating the impact of management responses on consumer reviews. *Marketing Science*, 36(5), 645-665. [doi.org/10.1287/mksc.2017.1043](https://doi.org/10.1287/mksc.2017.1043).
11. Xie, K. L., Zhang, Z., & Zhang, Z. (2014). The business value of online consumer reviews and management response to hotel performance. *International Journal of Hospitality Management*, 43, 1-12. [doi.org/10.1016/j.ijhm.2014.07.007](https://doi.org/10.1016/j.ijhm.2014.07.007).

### Regulation and Local AI Registry sources

12. U.S. Federal Trade Commission. (2024). Trade Regulation Rule on the Use of Consumer Reviews and Testimonials, 16 CFR Part 465. *Federal Register*, 89, 68034 (22 August 2024). [federalregister.gov](https://www.federalregister.gov).
13. Local AI Registry Research Team. (2026). How often AI recommends your business: A better measure of local visibility. [localairegistry.com/research/how-often-ai-recommends-your-business](https://localairegistry.com/research/how-often-ai-recommends-your-business).
14. Local AI Registry. (2026). Methodology: How the AI Score is built. [localairegistry.com/methodology](https://localairegistry.com/methodology).

The findings described in this brief belong to the original authors. Local AI Registry selected, grouped and explained them, and made the figures. Figures 1 and 4 are conceptual figures of our own.

## How to cite this research

```
Local AI Registry Research Team (2026). Why AI Chooses One Business Over Another: What Three Controlled Experiments Show (LAIR-R-2026-005). Local AI Registry. https://localairegistry.com/research/why-ai-chooses-one-business-over-another
```

Figures 2 and 3 have a “Data behind this chart” table, and their values are available as a [CSV download](https://localairegistry.com/research/why-ai-chooses-one-business-over-another/data/why-ai-chooses-one-business-over-another-data.csv). Every value is the original authors’ published estimate.

## About the author

The Local AI Registry Research Team is the research group of Local AI Registry, an answer engine optimization company for local businesses based in Irvine, California. It publishes studies on how AI assistants such as ChatGPT, Gemini, Claude and Perplexity find and describe local businesses.

One last thing

AI is evolving every day. So is our playbook.

The engines change how they find, read and cite local businesses constantly, and what worked last quarter may not work next quarter. At Local AI Registry, our dedicated local AI research team keeps testing what works, so the businesses we serve always get the current best approach.
