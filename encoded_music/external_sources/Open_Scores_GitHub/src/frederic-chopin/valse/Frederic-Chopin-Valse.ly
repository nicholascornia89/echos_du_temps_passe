\version "2.25.20"

#(ly:set-option 'relative-includes #t)

\include "./covercolor.ly"

\header {
  tagline = ##f
}

\paper {
  #(set-paper-size "a4")
  annotate-spacing = ##f
  binding-offset = 0\mm
  bottom-margin = 5\mm
  first-page-number = 0
  indent = 0.0
  %inner-margin = 10\mm
% last-bottom-spacing.padding = #2
  %left-margin = 10\mm
  line-width = 19\cm
  markup-system-spacing =
     #'((basic-distance . 2)
        (minimum-distance . 1)
        (padding . 2)
        (stretchability . 24))
  %outer-margin = 20\mm
  print-all-headers = ##t
  ragged-last-bottom = ##f
  ragged-bottom = ##f
  %right-margin = 10\mm
  score-markup-spacing =
     #'((basic-distance . 10)
        (minimum-distance . 8)
        (padding . 2)
        (stretchability . 24))
  system-system-spacing =
     #'((basic-distance . 2)
        (minimum-distance . 1)
        (padding . 2)
        (stretchability . 24))
  top-margin = 10\mm
  top-markup-spacing.basic-distance = 0
  top-system-spacing.basic-distance = 1
}

\bookpart {
  \header {
    maintainer      = "Davide Madrisan"
    maintainerEmail = "d.madrisan@proton.me"
  }

  \include "./header.ily"
  \header {
    title = ##f
    composer = ##f
  }

  \markup {
    \with-dimensions #'(0 . 0) #'(0 . 0)
    \with-color \coverColor
    \filled-box #'(-200 . 200) #'(-200 . 200) #0
  }
  \markup {
    \fill-line {
      \center-column {
        \null\null\null\null
        \null\null\null\null
        \line { \abs-fontsize #30 \bold "Frédéric" }
        \null
        \line { \abs-fontsize #80 \bold "Chopin" }
        \null
        \fill-line { \draw-hline }
        \null\null\null
        \line { \abs-fontsize #40 \bold "Valse in A minor" }
        \null\null\null\null\null
        \fill-line \italic { \abs-fontsize #14 "For Piano" }
        \null\null\null
        \null\null\null
        \null\null\null
      }
    }
  }

  \include "./logo.ly"

  \markup {
    \fill-line {
      \center-column {
        \null\null\null\null
        \fill-line {
          \abs-fontsize #10 "Based on the manuscript found in 2024 at the Morgan Library & Museum in New York"
        }
        \null\null
      }
    }
  }
}

\pageBreak

\markup \center-column {
  \vspace #2
  \line {
    \hspace #1.5
    \general-align #Y #DOWN {
      \image #X #105 #"chopin-valse-manuscript-2024.png"
    }
  }
}
\markup {
  \fill-line {
    \center-column {
      \null\null
      \fill-line \abs-fontsize #10 {
        \italic "The manuscript found in 2019 at the Morgan Library & Museum in New York"
      }
    }
  }
}

\markup {
  \hspace #0
  \column {
    \null\null\null
    \wordwrap \abs-fontsize #11 {
      Artur Szklener, Director of the \italic { Fryderyk Chopin Institute,}  has noted
      \italic { features of the brilliant style } consistent with the composer's activity in the first half
      of the 1830s, and suggested that the manuscript's neatness argues against it having been co-written
      with a student during a lesson, while highlighting the absence of dedication and signature
      – the word \italic Chopin is not written in his hand –
      as might be expected of a gift of a manuscript of this type.
      \hspace #1
      The relatively numerous performance indications
      (such as \italic sforzato, \italic { sempre forte } or finally \italic fortississimo),
      the appearance of fingering markings in such a short and simple passage for the pianist are quite
      surprising, but could indicate that the manuscript might have been given to an amateur pianist.
      \hspace #1
      He regards the piece as more likely a \italic { sketch of the first musical thought, }
      \italic { a trace of Chopin's activity in the pianistic community, }
      than a complete work, while accepting that the ornamentation of the melody and accompaniment's
      \italic { shifting seconds } are hallmarks of the composer's language, albeit combined
      with the overrepresentation of almost banal features, such as the nearly exclusive \italic a
      sound in the bass or the extremely simple figures that hark back to the brilliant style,
      but also deviate even from Chopin's Warsaw compositions.
   }
    \null\null
    \line \abs-fontsize #11 {
      [ \italic { freely taken from Wikipedia and an article by Dr Artur Szklener }]
    }
  }
}
\pageBreak

Global = {
  \key a \minor
  \time 3/4
  \include "global.ly"
}

Soprano = \context Voice = "one" \relative c' {
  \voiceOne
  \stemUp\tieUp
  \override MultiMeasureRest.staff-position = #0
  \override Rest.staff-position = #0
  \override Stem.cross-staff = ##t
  %\omit TupletNumber
  \repeat volta 2 {
  \partial 4 s4
  %1
  | s2.
  | s2
    \override Hairpin.to-barline = ##f
    \once\override Hairpin.shorten-pair = #'(0 . 1.4)
    \crossStaff { f4^\fz\> }
  | \crossStaff { e\! } s2
  | \repeat unfold 3 {
      s2 \crossStaff { f4^\fz }
    }
  %6
  | \stemNeutral <d'' f>8^>\fff ais^2 <b d>^>[ f^1] <gis b>^> e
  | \once\override Staff.TextScript.extra-offset = #'(0 . -2)
    <eis gis>8_\markup {
      "sempre " \dynamic f
    }
    cis <d f!>[ ais] <b d> f
  | e2^> a4
  | \tuplet 3/4 { gis16( a gis } fisis8 gis a b)
  %10
  | e,2 c'4
  | \stemUp \grace { b16 c } \stemNeutral b4 ais8 b c d
  | e4 <a c e>8( e <a c e> dis,
  | <a'	c e>8 d,) e[( c] e b)
  \break
  | \tuplet 3/4 { a16 b a } gis8[ a d8. c16]
  %15
  | b8[( e e, e]) \once\slurDown \appoggiatura g16 f8. e16
  | e2 a4
  | \tuplet 3/4 { gis16( a gis } fisis8 gis a b)
  | c4\rest \stemUp c2~
  | c8 b\trill a[ b <a c> <b d>]
  %20
  | e4. e8  e4
  | \grace d,8 e'4. e8  d4
  | c8 e, dis c' d, b'
  | <c, a'>4 r
  }
    \fine
}

Alto = \context Voice = "two" \relative c' {
  \voiceTwo
  \stemDown\tieDown
  \override Rest.staff-position = #0
  \partial 4 s4
  %1
  | s2.*18
  | e2 f8 fis
  %20
  | g2 f4
  | <e g c>2.
  | s4 f2
}

Tenor = \context Voice = "three" \relative c' {
  \voiceThree
  \stemUp\tieUp
  \override Rest.staff-position = #0
  \override Stem.cross-staff = ##t
  \partial 4 a4
  %1
  | g4\rest^\p
    \once\shape #'((0 . 0) (0 . 4) (0 . 5) (-0.5 . 5.5)) PhrasingSlur
    e8\( c' dis, c'
  | d, b' f b
    \crossStaff { gis4\) }
  | \crossStaff { a }
    \once\shape #'((0 . 0) (0 . 4) (0 . 5) (-0.5 . 5.5)) PhrasingSlur
    e8\( c' dis, c'
  | d, b' f b \crossStaff { gis4\) }
  %5
  | d8 b' f b \crossStaff { gis4 }
  | d8^\markup { "cresc." }
    b' f b \crossStaff { gis4 }
  | s2.*14
  %21
  | c4\rest <e, g c> q
  | c'\rest b c\rest
  | c\rest fis, gis4
}

Bass = \context Voice = "four" \relative c {
  \repeat volta 2 {
  \voiceFour
  \stemDown\tieDown
  \override MultiMeasureRest.staff-position = #0
  \override Rest.staff-position = #0
  \partial 4 s4
  %1
  | <a, a'> c\rest q
  | q c\rest <a' d>
  | <a c> e\rest <a, a'>
  | \repeat unfold 3 {
      <a a'> e'\rest <a d>
    }
  %7
  | <a d f b>4 q q
  | <a f' b> q q
  | a4 <e' c'> q
  %10
  | a, <e' d'> q
  | a, <e' c'> q
  | a, <e' gis d'> q
  | a, <e' c'> q
  | a, <e' gis d'> q
  %15
  | a, <e' c'> q
  | e, <e' gis d'> q
  | a, <e' c'> q
  | a, <e' d'> q
  | a, <e' c'> aes,
  %20
  | g <g' d'> q
  | c,2.
  | d2 b4
  | \once\stemUp \slashedGrace e,8 e'2.
  | a4 a,
  }
    \fine
}

\score {
  \new PianoStaff
  <<
    \accidentalStyle Score.piano
    \context Staff = "upper" <<
      \set Staff.midiInstrument = #"acoustic grand"
      \Global
      \clef treble
      \Soprano
      \Alto
    >>
    \context Staff = "lower" <<
      \set Staff.midiInstrument = #"acoustic grand"
      \Global
      \clef bass
      \Tenor
      \Bass
    >>
  >>
  \header {
    composer = "Frédéric Chopin"
    opus = "1830-1835 (?)"
    title = \markup { "Valse" }
    subtitle = ##f
  }
  \layout {
    \context {
      \PianoStaff
      \consists "Span_stem_engraver"
      \override Parentheses.font-size = #-2
      \override TextScript.font-shape = #'italic
      \override TextScript.font-size = #-1
    }
  }
  \midi {
    \tempo 4 = 100
  }
}
