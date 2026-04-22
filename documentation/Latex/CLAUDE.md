# LaTeX Editing Rules — RLCV4 Technical Documentation

When editing or creating LaTeX content for this project, the following rules are mandatory.
The project document class is `article`, compiled with `pdflatex -shell-escape`.
The main file is `documentation/Latex/main.tex`.

## 1. Abbreviation Management
- Before using any technical abbreviation (e.g., MCU, DMX, PCB, ISR, UART, I2C, SPI, PWM, FreeRTOS, ADC, DAC, GPIO, DMA, OLED, USB, RS485),
  check whether it already exists in the `\begin{acronym}...\end{acronym}` block in `main.tex`.
- If it **does not exist**, add an entry in the correct alphabetical position:
  ```latex
  \acro{MCU}{Microcontroller Unit}
  ```
- **Always** use `\ac{MCU}` in the text body — never write out the full form manually or the bare abbreviation without `\ac{}`.
- The acronym block must be inside an unnumbered section:
  ```latex
  \section*{Abbreviations}
  \begin{acronym}[LONGEST]
    \acro{...}{...}
  \end{acronym}
  ```
- If the acronym block does not exist in `main.tex` yet, create it before `\end{document}`.

## 2. Technical Language
- Use precise, domain-specific vocabulary. No colloquial phrasing.
- Write in passive or impersonal third-person: "The signal is filtered…", not "We filter the signal…".
- Define quantities with full physical context on first use.
- Do not hedge with "might", "could", "perhaps" — state facts directly.

## 3. Physical Quantities and Units
- Use `siunitx` for **all** numerical values with units:
  ```latex
  \SI{24}{\volt}   \SI{10}{\kilo\ohm}   \SI{115200}{\baud}   \SI{4}{\mega\hertz}
  ```
- Never write `24V`, `10kΩ`, or plain text units.
- For standalone units: `\unit{\kilo\ohm}`.

## 4. Code Listings
- Always use `minted`, never `verbatim`, `lstlisting`, or any other environment.
- Wrap in `tcolorbox` via the project's pre-configured hook (already set up in preamble).
- Specify the correct language lexer: `{cpp}`, `{c}`, `{bash}`, `{text}`, etc.
- Listings must include the following style configurations:
  - `linenos`: Line numbers on the left.
  - `frame=leftline`: A vertical separator line between numbers and code.
  - `xleftmargin`: Sufficient margin (e.g., `20pt`) to clear line numbers.
  - Labeled as **Sourcecode** (via `\renewcommand{\listingscaption}{Sourcecode}`).
- For floating listings use the `longlisting` environment with a `\caption{}` and `\label{lst:name}`.

## 5. Figures
- All images must be in `documentation/Latex/graphics/`.
- Always include `\label{fig:name}` and `\caption{...}` inside the `figure` environment.
- Reference with `\ref{fig:name}` — never use hardcoded numbers.
- Use `[H]` placement specifier (requires `float` package, already loaded).
- Example:
  ```latex
  \begin{figure}[H]
    \centering
    \includegraphics[width=0.8\textwidth]{schematic_overview}
    \caption{Schematic overview of the power supply section.}
    \label{fig:schematic_overview}
  \end{figure}
  ```

## 6. Tables
- Use `\hline` to separate rows.
- **Never** use `booktabs` commands like `\toprule`, `\midrule`, or `\bottomrule`.
- Use `tabularx` with `X` columns for auto-width, or `tabular` for fixed-width.
- Always include `\label{tab:name}` and `\caption{}`.
- Avoid creating tables for only one or two items; prefer incorporating this information directly into the text.
- Place caption **above** the table.
- Example:
  ```latex
  \begin{table}[H]
    \caption{Pin assignment of the RS-485 interface.}
    \label{tab:rs485_pins}
    \centering
    \begin{tabularx}{\textwidth}{|X|X|X|}
      \hline
      \textbf{Pin} & \textbf{Signal} & \textbf{Description} \\ \hline \hline
      1 & A & Non-inverting data line \\ \hline
      2 & B & Inverting data line \\ \hline
    \end{tabularx}
  \end{table}
  ```

## 7. Sections and Cross-References
- Add `\label{sec:name}` immediately after every `\section{}`, `\subsection{}`, `\subsubsection{}`.
- Reference sections with `Section~\ref{sec:name}`, figures with `Figure~\ref{fig:name}`, tables with `Table~\ref{tab:name}`.
- Use `~` (non-breaking space) before all `\ref{}` calls.

## 8. Equations
- Number all standalone equations with the `equation` environment.
- Add `\label{eq:name}` to every equation.
- Reference with `Equation~\eqref{eq:name}`.
- Use `align` for multi-line derivations.
- Use `\cdot` for multiplication; never use `\times` for scalar multiplication.

## 9. Citations
- Cite all external claims with `\cite{key}` using the `natbib` package (numeric style).
- Do not invent citation keys — only reference keys that exist in the `.bib` file.
- Place citations before the sentence period: "…as described in \cite{key}."

## 10. TikZ and circuitikz Environments
- **Never** use `\ac{...}` inside any `tikzpicture` or `circuitikz` environment.
  The `acronym` package expands `\ac{}` on first use to the full long form (e.g. `\ac{UART}` → "Universal Asynchronous Receiver-Transmitter (UART)"), which overflows node boxes and breaks diagram layout.
- Use plain abbreviated text directly in node labels: write `UART`, `I2C`, `OWI`, `PWM`, `USB`, etc.
- `\ac{...}` remains mandatory everywhere else in the document body (paragraphs, captions, table cells, list items).

## 11. Circuit Diagrams
- Use `circuitikz` for all schematic diagrams.
- Always use the `european` style for components (e.g., rectangular resistors).
- Wrap in `tcolorbox` via the project's pre-configured hook (already set up in preamble).

## 12. Block Diagrams (TikZ / circuitikz)
- Use `circuitikz` with `[>=latex]` for arrow heads.
- Draw bounding boxes or backgrounds with `[dashed, thick, fill=gray!5, rounded corners]`.
- Style nodes with `[draw, fill=white, minimum width=..., minimum height=..., rounded corners]`.
- Use `\draw[-latex, thick]` for straight arrows; add `rounded corners=4pt` for orthogonal (`|-` / `-|`) paths so the bend is visually smooth.
- **Always** add `rounded corners=4pt` (or similar) to any `\draw` that uses `|-` or `-|` routing.
- Use explicit coordinates or orthogonal paths `|-` and `-|` for clean layout.
- Example:
  ```latex
  \begin{circuitikz}[>=latex]
    % Background
    \draw[dashed, thick, fill=gray!5, rounded corners] (0, 0) rectangle (6, 4);
    \node[anchor=north] at (3, 4) {\textbf{System Block}};

    % Nodes
    \node[draw, fill=white, minimum width=2.8cm, minimum height=0.8cm, rounded corners] (in) at (-3, 2) {Input};
    \node[draw, fill=white, minimum width=2cm, minimum height=0.6cm, rounded corners] (proc) at (3, 2) {Process};

    % Connections
    \draw[-latex, thick, rounded corners=5pt] (in.east) -- (proc.west);
  \end{circuitikz}
  ```

## 13. Sentence Formatting
- Every sentence must start on its own line in the `.tex` source.
- Do not place multiple sentences on the same line.
- A blank line (paragraph break) remains a blank line — this rule applies within a paragraph, not between them.
- Example:
  ```latex
  The LMR54410 feeds \SI{3.3}{\volt} directly to the ESP32-S3-MINI-1-N8 module.
  The XIAO board and its onboard \ac{LDO} are eliminated.
  No topology change is required relative to Revision~1 — only the feedback resistors and current rating differ.
  ```

## Workflow When Editing
1. **Read** the target `.tex` file and the acronym block in `main.tex` before making any change.
2. Identify all abbreviations in the new/modified text.
3. Add missing acronym entries to the acronym block (alphabetically).
4. Replace all bare abbreviations and spelled-out forms in the text with `\ac{...}`.
5. Apply all other rules (units, labels, code style, table style).
6. Do not change unrelated parts of the file.

## Common RLCV4-Specific Acronyms
See the `\begin{acronym}` block in `main.tex` for the definitive list of existing acronyms.
