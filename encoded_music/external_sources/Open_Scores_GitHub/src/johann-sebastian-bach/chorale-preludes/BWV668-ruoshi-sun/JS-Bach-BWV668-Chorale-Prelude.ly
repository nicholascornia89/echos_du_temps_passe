\version "2.25.16"

#(ly:set-option 'relative-includes #t)

\include "./covercolor.ly"
\include "./macros.ly"

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
        \line { \abs-fontsize #30 \bold "Johann Sebastian" }
        \null
        \line { \abs-fontsize #80 \bold "Bach" }
        \null
        \fill-line { \draw-hline }
        \null\null\null
        \line { \abs-fontsize #28 \bold "Vor deinen Thron tret' ich hiermit" }
        \null
        \line { \abs-fontsize #18 "(Before your throne I now appear)" }
        \null\null\null\null
        \line { \abs-fontsize #24 "BWV 668" }
        \null\null\null\null\null\null
        \fill-line { \abs-fontsize #12 "Transcribed for Piano Solo by Ruoshi Sun" }

        \null\null\null
        \null\null\null
      }
    }
  }

  \include "./logo.ly"

}

Global = {
  \key g \major
  \time 4/4
  \include "./global.ly"
}

Sopran = \context Voice = "one" \relative c'' {
  \voiceOne
  \override MultiMeasureRest.staff-position = #5
  \override Rest.staff-position = #0
  %1
  | R1*7
  | \highlightCFOrn { g2^\markup {
      \hspace #2 "c.f. [cum ornamentis]"
    }
    g4 a8 c16 b
  | b4 a8. b16 c4 b
  %10
  | a4~\trill a16 g a8 g2~
  | g } f'\rest
  | R1*7
  %19
  | f2\rest \highlightCF { b,
  | c4 \stemDown b a \stemUp g
  | fis g \unHighlightCF a2~ }
  | a f'\rest
  | R1*3
  | \once\override Voice.MultiMeasureRest.X-offset = #1.4 R1
  | R1*2
  %29
  | f2\rest \highlightCF { d
  | c4 b a8 g fis4
  | g8 fis e4 \once\override Tie.staff-position = #-2 \unHighlightCF d2~ }
  | d f'2\rest
  | R1*7
  %40
  | f2\rest \highlightCF { b,
  | c4 b a g8 a
  | b4 a \unHighlightCF g2~ }
  | g1~
  | g~
  %45
  | g\fermata
  \fine
}

Alto = \context Voice = "two" \relative c'' {
  \voiceTwo
  \override MultiMeasureRest.staff-position = #-2
  \override Rest.staff-position = #0
  \override VoiceFollower.color = \greyTextColor
  \override VoiceFollower.style = #'dashed-line
  \showStaffSwitch
  \stemNeutral\tieNeutral
  %1
  | R1
  | r8 \highlightCFInv {
    g_\markup {
     \whiteout "c.f. [per dimin., inversus]"
    }
    g fis e4 fis8 e
  | d e fis4 g4. } fis8
  | e a d, g~ g fis16 e fis8 g
  %5
  | a4 g8 a b \highlightCFInv { d,[ d cis]
  | b4 cis8 b a b cis4
  | d4. } c16 b c4. b16 a
  | \stemDown\tieDown b8 b[ b c] d4 e8 fis
  | g b, e d c d d4
  %10
  | e8 c d c b c d4~
  | d8 c16 b c8 a b e\rest e4\rest
  | \stemNeutral\tieNeutral r8 \highlightCFInv { e d e fis g a g
  | fis4 } g8 gis a g fis e16 dis
  | e2.~ e8 d16 cis
  %15
  | d8 \highlightCF { fis[ g fis] e d cis dis
  | e4. } fis16 g a4. g16 fis
  | g4. fis16 e fis8 d g4^~
  | g^~ g16 e d e fis8 g a g16 fis
  | \stemDown g8 d[ d e] f g16 f \change Staff = "lower" \stemUp e8 d
  %20
  | c \change Staff = "upper" \stemUp g'[ g fis]
    \once\override NoteColumn.force-hshift = #0.2 e fis
    \highlightCF { \unHighlightCF \stemDown g4 }
  | \once\override Rest.extra-offset = #'(0.6 . 0) g,8\rest d'[ d cis16 b] e8 cis16 d e8 cis
  | d16 e fis8 \stemUp e16 fis g8 fis f\rest f4\rest
  | \stemNeutral\tieNeutral r2 r8 \highlightCFInv { a, b cis
  | d4 f e8 fis gis4
  %25
  | \unHighlightCF a8 } f e d cis16 dis e4 dis8
  | e8. fis16 g8. a16 \once\stemUp b8 a4 b16 a
  | g4 a d, e
  | fis8 a g fis e d c4
  | \stemDown\tieDown b8 d g4 fis8 fis[ fis g]
  %30
  | a fis d2.~
  | d8 d4 cis8 d4. c8
  | b2~ b8 a e'4\rest
  | \stemNeutral\tieNeutral r8 e d e fis g16 fis e8 fis
  | g4. fis16 e fis8 b, e4~
  %35
  | e dis e8 \highlightCF { fis[ g fis]
  | e8 d16 e fis8 e d4. } \highlightCFInv { c8
  | b cis d e16 d cis8[ d] \unHighlightCF e } fis16 e
  | d8 e fis gis a4 a\rest
  | r8 \highlightCF { a b a g fis16 g a8 g
  %40
  | \stemDown\tieDown fis4 } e8 fis16 g fis2
  | e8 fis g4~ g8 fis g fis
  | g4. fis8~ fis \highlightCF { e f e
  | d c16 d e8 d c } c\rest c4\rest
  | b4 b\rest b8\rest \highlightCF { b c b
  %45
  | a8 g16 a b8 a g2\fermata }
}

Tenor = \context Voice = "three" \relative c' {
  \voiceThree
  \override MultiMeasureRest.staff-position = #0
  \override Rest.staff-position = #0
  \override VoiceFollower.color = \greyTextColor
  \override VoiceFollower.style = #'dashed-line
  \showStaffSwitch
  \stemNeutral\tieNeutral
  %1
  | r8 \highlightCF {
      g^\markup {
        \whiteout "cantus firmus [per diminutionem]"
      }
    g a b4 a8 b
  | c b a4 \unHighlightCF g8 } gis a ais
  | b4. a8 b cis d4~
  | \stemUp\tieUp d8 c b e a,2~
  %5
  | a8 b c4 b8 a g4~
  | g8 fis g gis a4. g8
  | a8 g16 fis g4~ g8 fis16 e fis4
  | a8\rest g g a b4 cis8 dis
  | e g,[ g fis] e a4 g8~
  %10
  | g g4 fis8 g g[ g f]
  | e4. 	ees8 d \highlightCF { b'[ c b]
  | a g fis g \unHighlightCF a } b c4~
  | c b e, a~
  | a8 g16 fis g4. fis16 e fis4~
  %15
  | fis g8\rest fis g gis a4~
  | a8 g16 fis g4. fis16 e fis8 b
  | e,4. a8 d,4 \change Staff = "upper" \stemDown b'16\rest d e d
  | c8 b a
    \hideStaffSwitch \change Staff = "lower" \stemUp b c4. b16 a
  | b8 b[ b c] e4 \showStaffSwitch \change Staff = "upper" \stemDown\tieDown g4~
  %20
  | g8 \change Staff = "lower" \stemUp\tieUp g,16[ a] b8
    \hideStaffSwitch \change Staff = "upper" \stemDown c16 d
    \once\override NoteColumn.force-hshift = #0.2 e8 d
    \once\override NoteColumn.force-hshift = #0.4 d8 e16 d
  | c8 \change Staff = "lower" \stemUp b16 a b8 g~ g g16 fis e8 fis16 g
  | a8 d4
   \showStaffSwitch \change Staff = "upper" \stemDown cis8 \highlightCF { d
   \change Staff = "lower" \stemUp
   d[ c b]
  | a4 fis g8 fis e4
  | \unHighlightCF d8 } c' b a gis a b4
  %25
  | \change Staff = "upper" \stemDown c b
    \change Staff = "lower" \stemUp e,16[ fis g8
    \hideStaffSwitch \change Staff = "upper" \stemDown\tieDown
    a b]
  | c4 e dis8 e fis4~
  | fis8 e[
    \change Staff = "lower" \stemUp
    d c] b4 cis
  | \showStaffSwitch \change Staff = "upper" \stemDown
    d2
    \change Staff = "lower" \stemUp\tieUp
    a8\rest d, e fis
  | g a b cis d c b4
  %30
  | d8\rest a a g fis b a4
  | g8 a b^\markup { "m.d." } a~ a fis g a~
  | a g16 fis g4~^\markup { "m.s." } g8 fis \highlightCF { b4
  | c b a g8 a
  | b4 a g2 }
  %35
  | fis8 g
    \change Staff = "upper" \stemDown\tieDown
    a b16 a g8 a b4~
  | b ais b8
    \change Staff = "lower" \stemUp\tieUp
    \highlightCFInv { fis[ e fis]
  | \change Staff = "upper" \stemDown
    g a16 g fis8 gis \unHighlightCF a } b16 a g8 a
  | b cis d4 cis8
    \change Staff = "lower" \stemUp\tieUp
    \highlightCF { fis,[ g fis]
  | e8 d16 e fis8 e d4 } c'\rest
  %40
  | c8\rest \highlightCF { b c b a g16 a b8 a
  | \unHighlightCF g } a b c16^\markup { "m.d." } d e8 d[ d c]
  | d4 e8 b b4. c8
  | g4 a8\rest b c \highlightCFInv { c,[ b c]
  | d e16 d c8 d e } \highlightCF { f[ g f]
  %45
  | ees8 d16 ees f!8 e \unHighlightCF d2\fermata }
}

Bass = \context Voice = "four" \relative c {
  \voiceFour
  \override MultiMeasureRest.staff-position = #-7
  \override Rest.staff-position = #0
  %1
  | R1*3
  | g2\rest g8\rest \highlightCF { d' d e
  %5
  | fis4 e8 fis g fis e4
  | \unHighlightCF d8 } dis e eis fis4. e8
  | fis b, e4~ e8 a, d4
  | g,8 g\rest g4\rest g8\rest g' g fis
  | e8. d16 c8 d a fis g b
  %10
  | c a d d, e e' b a16 b
  | c2 g8 g\rest g4\rest
  | \override MultiMeasureRest.staff-position = #-6
    R1
  | a8\rest \highlightCF { d e d c b a b
  | c4. } b16 ais b2~
  %15
  | b4 a\rest a8\rest \highlightCFInv { b a b
  | c d e d \unHighlightCF cis } a d4~
  | d8 cis16 b cis8 c~ c b16 a b8 g
  | a8 b16 c d4~ d8 e fis d
  | g2~ g8 g[ g f]
  %20
  | e e[ e d] c c[ c b]
  | a d b[ e] cis a16 b cis8 a
  | fis' d a'[ a,] d a\rest a4\rest
  | R1
  | g2\rest a8\rest d c b
  %25
  | a4 gis a8 g fis4
  | e8 a g[ c] b cis dis b
  | e4 fis g,8\rest \highlightCF { g' fis e
  | d4 b c8 b a4
  | \unHighlightCF g8 } fis e a d, d'[ d e]
  %30
  | fis d g[ g,] d' d[ d cis]
  | b a g a16 g fis8 d e fis
  | g a b cis d4 g,\rest
  | R1
  | a8\rest \highlightCF { c_\markup {
      \whiteout "c.f. [per diminutionem]"
    }
    d c b a16 b c8 b
  %35
  | a4 } b e, e'8 d
  | cis4 fis,8 fis' b, a g a
  | e4 b' a g\rest
  | g\rest \highlightCFInv { b a b
  | cis d8 cis b4 cis
  %40
  | \unHighlightCF d8 } dis e2 dis4
  | e8 e[ e d] c d16 c b8 a
  | g b cis dis e, e' d c
  | b a16 b c8 g e fis g a
  | b g a b c2~
  %45
  | c g\fermata
  \fine
}

Choral = \relative {
  \autoBeamOff
  \time 12/2
  \key g \major
  \override Score.BarNumber.break-visibility = ##(#f #f #f)
  \override Staff.NoteHead.style = #'baroque
  \once\override Staff.TimeSignature.stencil = ##f
  g'1 g2 a b( a4 b c2) b a2. a4 g1 \bar "'"
  \time 10/2
  \once\override Staff.TimeSignature.stencil = ##f
  b1 c2 b a g fis g a1 \bar "'"
  \break
  d1 c2 b a4( g) fis2 g4( fis) e2 d1 \bar "'"
  \once\override Staff.TimeSignature.stencil = ##f
  b'1 c2 b a g4( a) b2 a g1
  \fine
}

\markup {
  \fill-line {
    \override #'(baseline-skip . 2)
    \center-column {
      \line { \abs-fontsize #14 \bold "Vor deinen Thron tret' ich hiermit" }
      \null
      \line {
        \abs-fontsize #8 \italic
        \concat {
          "Genf 1547 von Loys Bourgeois (" \char ##x2055 " um 1515 Paris, Kantor zu Genf / St. Pierre, "
          \char ##x2020 " nach 1561 [Paris?])"
        }
      }
      \null
      \line {
        \score {
          <<
          \new Voice = "corale" {
            \override VerticalAxisGroup.staff-staff-spacing.basic-distance = #1
            \Choral
          }
          \new Lyrics \lyricsto "corale" {
            \override VerticalAxisGroup.nonstaff-relatedstaff-spacing.padding = #1
            \override VerticalAxisGroup.nonstaff-relatedstaff-spacing =
              #'((basic-distance . 4))
            << {
              Vor dei -- nen Thron __ tret ich hier -- mit,
              o Gott, mit in -- nig -- li -- cher Bitt:
              ach, kehr dein lieb -- reich
              An -- ge -- sight von mir blut -- ar -- men Sün -- der nicht!
            }
            \new Lyrics {
              \set associatedVoice = "corale"
              Be -- sche -- re mir __ ein se -- lig End;
              nimm mei -- ne Seel in dei -- ne Händ,
              daβ ich dich schau dort e -- wig -- licht
              Ja, A -- men, ja, er -- hö -- re mich!
            } >>
          }
          >>
          \layout {
            indent = #0
            line-width = #150
            #(layout-set-staff-size 14)
          }
        }
      }
      \null\null
      \line {
        \abs-fontsize #8 \italic
        \concat {
          "Bodo von Hodenberg (" \char ##x2055 " 1604 Celle, "
          \char ##x2020 " 1650 als Landdrost und Berghauptmann zu Osterode am Harz)  (*)"
        }
      }
      \null\null\null\null\null
    }
  }
}

\score {
  \new PianoStaff
  <<
    \accidentalStyle Score.piano
    \context Staff = "upper" <<
      \set Staff.midiInstrument = #"acoustic grand"
      \Global
      \clef treble
      \Sopran
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
    composer = ##f % "Johann Sebastian Bach"
    opus = ##f % "BWV 668"
    title = \markup { "Vor deinen Thron tret' ich hiermit" }
    subtitle = \markup {
      \column {
        \line { "Chorale Prelude" }
        % workaround to insert some vertical space after the subtitle
        \line { " " }
      }
    }
  }
  \layout {
    \context {
      \PianoStaff
      \override Parentheses.font-size = #-2
      \override TextScript.font-shape = #'italic
      \override TextScript.font-size = #-1
    }
  }
  \midi {
    \tempo 4 = 38
  }
}

% Before your throne I now appear,
% O God, and beg you humbly
% Turn not your gracious face
% From me, a poor sinner.
% Confer on me a blessed end,
% On the last day waken me Lord,
% That I may see you eternally:
% Amen, amen, hear me.

\markup {
  \footnote ""
  \column \small\italic {
     \line {
       \concat {
         "*" \hspace #.3 \vspace #1
         "Before your throne I now appear, "
       }
     }
     \line {
       \concat {
         " " \hspace #.3 \vspace #1
         "O God, with fervent supplication:"
       }
     }
     \line {
       \concat {
         " " \hspace #.3
         "Alas, turn not thy loving "
         "Face from me, poor sinner!"
       }
     }
     \line {
       \concat {
         " " \hspace #.3
         "Grant me a blessed end; "
       }
     }
     \line {
       \concat {
         " " \hspace #.3
         "Take my soul into your hands, "
         "that I may behold thee there eternally bright. "
       }
     }
     \line {
       \concat {
         " " \hspace #.3
         "Yes, amen, yes, hear me!"
       }
     }
  }
}
