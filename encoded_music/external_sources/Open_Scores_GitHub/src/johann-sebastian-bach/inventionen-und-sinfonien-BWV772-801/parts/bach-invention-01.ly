Global = {
  \key c \major
  \time 4/4
  \include "../global.ly"
}

staffLower = { \change Staff = "lower" }
staffUpper = { \change Staff = "upper" }

voiceOneOssia = \relative c'' {
  %1
  | \stopStaff s2 s8. \startStaff s16 b32( a b16 c8)
  | d16 g, a b c a b g d'8[ g f32 e f16 g8]
    \stopStaff
  | s1*2
  %5
  | \startStaff a,8_. d,_. c'32-4( b c8 d16) \stopStaff s2
  | s2 s8. \startStaff
    \set subdivideBeams = ##t
    \set baseMoment = #(ly:make-moment 1/8)
    s16 c32-4( b c16 a g) \stopStaff
}

VoiceOne = \context Voice = "one" \relative c' {
  \voiceOne
  \override MultiMeasureRest.staff-position = #0
  \override Rest.staff-position = #0
  \stemNeutral\tieNeutral\slurNeutral
  %1
  | \override Score.MetronomeMark.Y-offset = #-4
  \tempo "Allegretto moderato" 4 = 84
    r16 c[ d e] f[ d e c] g'8-.[ c-4 b^\mordent c]
  | d16-.[ g, a b] c[ a b g] d'8-.[ g-4 f^\mordent g]
  | e16[ a g f] e[ g f a] g[ f e d-1] c-2[ e d f]
  | e[ d c b-1] a-2[ c b d] c[ b a g-1] fis-2[ a g b]
  %5
  | a8_.[ d,_.] c'8.[^\mordent d16] b-3[ a g fis] e[ g fis a-3]
  | g-1[ b a c] b-3[ d-5 c-2 e] d[ b32 c d16 g] b,8[^\parenthesize\prall a16 g]
  | g8 r r4 r16 g[ a b] c[ a b g]
  | fis8^\prall\finger \markup \tied-lyric "3-2-3" r r4 r16 a[ b c] d[ b c a]
  | b8 r r4 r16 d[ c b] a[ c b d]
  %10
  | c8 r r4 r16 e[ d c] b[ d cis e]
  | d8^.[ cis^. d^. e^.] f^.[ a,^. b!^.-3 cis^.]
  | d[_. fis,_. gis_. a_.-3] b^.-1[ c^.-3] d4~-5
  | d16[ e, fis gis] a[ fis gis e] e'-5[ d-3 c e] d[ c b-1 d-2]
  | c[ a' gis b] a[ e-1 f-4 d]
    gis,[ f' e d] c8-\finger \markup \tied-lyric "4-3-4"[\parenthesize\prall b16 a]
  %15
  | a16[ a' g f] e[ g f a] g2~
  | g16[ e f g] a[ f g e] f2~
  | f16[ g f e] d[ f e g] f2~
  | f16[ d e-3 f] g[ e f d] e2~
  | e16[ c d e] f[ d e c] d-2[ e-1 f g] a[ f g e]
  %20
  | f-2[ g-1 a b] c[ a b g] c8^.[ g^.] e\prall\finger \markup \tied-lyric "3-2-3"[ d16 c]
  | c-5[ bes a g] f[ a g bes]
    \once\override Staff.TextScript.extra-offset = #'(0 . -2)
    a[_\markup { "poco rall." } b c e,-2] d[ c' f, b]
  | %<c g e>1^\fermata\arpeggio
    <c g e>1^\fermata
    \fine
}

VoiceTwo = \context Voice = "two" \relative c {
  \voiceTwo
  \override MultiMeasureRest.staff-position = #0
  \override Rest.staff-position = #0
  \stemNeutral\tieNeutral\slurNeutral
  %1
  | r2 r16
    %\shape #'((0 . 0) (0 . 0.5) (0 . 0.5) (0 . 0.5)) Slur
    c[ d e] f[ d e c]
  | g'8-.[ g,-.] r4 r16 g'[ a b] c[ a b g]
  | c8^.[ b^.-4 c^. d^.] e^.[ g,^. a^. b^.]
  | c^.[ e,^. fis^.-3 g^.] a^.-1[ b^.-2] c4-1~
  %5
  | c16[ d, e fis] g[ e fis d] g8^.[ b,^. c^. d^.-3]
  | e^.-1[ fis^. g^. e^.] b8.-5[ c16-2] d8-.-1[ d,-.]
  | r16 g[ a b] c[ a b g] d'8^.[ g^. fis^.-3 g^.]
  | a16[ d, e fis] g[ e fis d] \clef "treble" a'8_.[ d_. c_.-3 d_.]
  | g,16[ g' f e] d[ f e g] f8_.[ e_. f_. d_.]
  %10
  | e16[ a g-2 f] e[ g f a] g8_.-3[ f_. g_. e_.]
  | f16[ bes_2 a_3 g] f[ a g bes_2] a_1[ g f e] d[ f e g_2]
  | f_1[ e d c] b[ d c e_2] d_1[ c b a] gis[ b a c_2]
  | \clef "bass"
  | b8^._1[ e,^.]
    \once\override Beam.positions = #'(-1 . 0)
    d'8._2[^\mordent \staffUpper e16]
    \staffLower\stemNeutral c_2[ b_3 a_1 g!] fis[ a gis_4 b]
  %15
  |  a[ c b_4 d] c[ e d_4 f] e8^.[ a,^. e'^. e,^.]
  | a8^.[ a,^.] r4 r16 e''16[ d c] b[ d cis e]
  | d2~ d16[ a-4 b c] d[ b c a]
  | b2~ b16[ d c b] a[ c b d]
  | c2~ c16[ g a_3 bes] c[ a bes g]
  %20
  | a8^.[ bes^. a^. g^.] f^.[ d'^. c^. bes^.]
  | a^.[ f'^. e^. d^.] e16[ d, e_3 f] g[ e f d]
  | e8^.[ c^. d^. e^.] f16[ d e f] g8_.[ g,_.]
  | %<\parenthesize c c,>1\arpeggio\fermata
    c,1\fermata
    \fine
}

\score {
  <<
  \new Staff = "ossia" \with {
    \include "../ossiasetup.ly"
    \hide Clef
    \remove Time_signature_engraver
  }
  { \voiceOneOssia }
  \new PianoStaff {
    \set Score.connectArpeggios = ##t
    <<
      \accidentalStyle Score.piano
      \context Staff = "upper" <<
        \set Staff.midiInstrument = #"acoustic grand"
        \Global
        \clef treble
        \VoiceOne
      >>
      \context Staff = "lower" <<
        \set Staff.midiInstrument = #"acoustic grand"
        \Global
        \clef bass
        \VoiceTwo
      >>
    >>
  }
  >>
  \header {
    composer = "Johann Sebastian Bach"
    opus = "BWV 772"
    title = \markup { "Invention I " \char ##x00b7 " C-Dur" }
    subtitle = \markup \normal-text \italic  {
      "Copyist Wilhelm Friedemann Bach (1720)"
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
    \tempo 4 = 84
  }
}
