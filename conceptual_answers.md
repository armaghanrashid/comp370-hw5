# Homework 5: Conceptual Questions

## 1. Use case for the technical exercise

**Persona:** the Deputy Director of Operations in the NYC Mayor's Office of Operations, who oversees how city agencies respond to 311 service requests.

**What hurts:** City Council members and community boards keep reporting that some neighbourhoods wait much longer than others for 311 complaints to be resolved. The office has no quick way to check these claims, so it cannot tell a real service gap from a few bad anecdotes.

**Decision the results feed:** Before each quarterly budget and staffing review, the Deputy Director will use the dashboard to compare the monthly average response time (hours from a complaint's creation to its closure) in any two zipcodes against the city-wide average for 2024. A zipcode that is consistently slower than the city average becomes a candidate for extra inspectors and crews, or for a follow-up review of the agencies that serve it. The CLI tool supports the same review: it shows which complaint types each borough files in a given period, so staff can see whether a slow zipcode is slow because of the type of complaints it gets.

## 2. Refining the My Little Pony question

Starting question: *"We'd like to understand how much characters talk across the My Little Pony series."*

Following Lesson 33: (1) find a representative for the stakeholders, (2) develop a use case (a persona and a concrete activity), and (3) iterate on the question, adding one detail at a time and looking at the data, until it is measurable and aligned with the use case. With no stakeholder to ask, I made each decision myself and give the reason for it.

**Step 1: Stakeholder representative.** A writer on a fan-run analysis blog about *My Little Pony: Friendship is Magic*, who speaks for the readers.

**Step 2: Use case.** The writer is preparing a post on whether the show gives its six main characters ("the Mane Six") equal screen time, and how this changed over the show's run. They will use the results to rank the Mane Six by how much each one talks and to show whether the ranking changes from season to season.

**Step 3: Iterating on the question.**

| # | Version of the question | What this step pinned down |
|---|---|---|
| 1 | How much do characters talk across the My Little Pony series? | (vague: which characters? what is "how much"? which part of the series?) |
| 2 | How much do **the six main ponies** (Twilight Sparkle, Rainbow Dash, Pinkie Pie, Applejack, Rarity, Fluttershy) talk across the series? | **Which characters.** The dataset has 842 different speaker names, most of them minor. The use case is about the Mane Six. |
| 3 | How much do the six main ponies talk **in the TV episodes** of *Friendship is Magic*? | **Which part of the series.** The transcripts also contain *My Little Pony: The Movie* and the special *Best Gift Ever*, which are not episodes. I exclude them. |
| 4 | What **share of all spoken lines** in the TV episodes belongs to each of the six main ponies? | **What "how much" means.** Spoken lines are what the transcript data records. Words or screen time would need other data. A share of all lines can be compared across episodes of different lengths. |
| 5 | What share of all spoken lines is spoken **by each of the six main ponies alone, under her main name**? | **What counts as one pony's line.** In the data, some lines have several speakers ("Rarity and Pinkie Pie"), some are spoken by groups ("Others", "All sans Twilight Sparkle"), and some characters appear under other names ("Twilight" vs "Twilight Sparkle"). I count only lines whose speaker field is exactly one main pony's full name. Shared lines and lines from alternate versions such as "Future Twilight Sparkle" are left out. |
| 6 | **For each season** of the TV episodes, what share of all spoken lines is spoken by each of the six main ponies alone, under her main name? | **The time breakdown.** The use case asks whether the balance changes over the run. Each episode title can be mapped to its season. |

**Final data science question:** *For each season of My Little Pony: Friendship is Magic (TV episodes only, not the movie or specials), what percentage of all spoken lines in the transcripts is spoken by each of the six main ponies (Twilight Sparkle, Rainbow Dash, Pinkie Pie, Applejack, Rarity and Fluttershy) alone, where a line counts for a pony only if the speaker field is exactly her full name?*

## 3. Why state maintenance is hard in a Jupyter notebook

A notebook's state lives in the kernel's memory: every variable, function and loaded dataset that exists at the moment. The code that created that state is spread across cells that can be run in any order, re-run, edited after running, or deleted. So the code on the page and the data in memory easily fall out of sync. For example:

- If I edit a cell but don't re-run it, the kernel still holds the old result, and later cells use values that the visible code no longer produces.
- If I run cells out of order, or delete a cell after running it, the notebook depends on state that no longer appears anywhere on the page. Restarting and running top to bottom then fails or gives different answers.
- If the kernel dies or restarts (for example after running out of memory, or when the session disconnects), all state is lost. Every cell has to be re-run, and expensive steps, such as reading a large dataset, have to be repeated.

A script, by contrast, runs from top to bottom every time, and anything that must persist is written to files on purpose. Keeping state in a script takes extra work, but you always know what produced it. A notebook gives no such guarantee.

## 4. Why a Jupyter notebook beats a README for sharing with future data scientists

A README describes the project. A notebook shows the analysis itself. In a notebook, the code, the explanation (markdown cells) and the outputs (tables, numbers, plots) are kept together in one document, in the order the analysis was done. A data scientist who opens it later can:

- **Orient quickly.** The notebook's embedded documentation makes orientation easy. The reader sees each step with its result directly under it. With a README they would have to install the project, find the right scripts, run them, and connect separate output files back to the code that made them.
- **Check the reasoning.** The saved outputs show what each step produced on the real data: intermediate tables, the shape of the data, and the plots that drove each decision. The reader can judge whether the method was sound without re-running anything. A README usually states conclusions and run instructions, but not the evidence.
- **Pick up the work.** The reader can re-run a cell, change a parameter or add a cell, and see the effect immediately in the same document. That makes it easy to extend the analysis rather than start over.

A README is still needed for installation and running instructions. But a data scientist who wants to understand, check and build on an analysis learns far more from a notebook than from a README.
