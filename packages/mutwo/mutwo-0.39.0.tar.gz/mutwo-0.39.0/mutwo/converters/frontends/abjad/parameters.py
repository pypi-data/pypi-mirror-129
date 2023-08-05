"""Module to convert mutwo parameters to abjad equivalents."""

import abc
import typing

try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore

import abjad  # type: ignore
import expenvelope  # type: ignore

from mutwo.converters import abc as converters_abc
from mutwo.converters.frontends.abjad import attachments
from mutwo.converters.frontends import ekmelily_constants

from mutwo import parameters

from mutwo.utilities import constants
from mutwo.utilities import tools

__all__ = (
    "MutwoPitchToAbjadPitchConverter",
    "MutwoPitchToHEJIAbjadPitchConverter",
    "MutwoVolumeToAbjadAttachmentDynamicConverter",
    "TempoEnvelopeToAbjadAttachmentTempoConverter",
    "ComplexTempoEnvelopeToAbjadAttachmentTempoConverter",
)


class MutwoPitchToAbjadPitchConverter(converters_abc.Converter):
    """Convert Mutwo Pitch objects to Abjad Pitch objects.

    This default class simply checks if the passed Mutwo object belongs to
    :class:`mutwo.parameters.pitches.WesternPitch`. If it does, Mutwo
    will initialise the Abjad Pitch from the :attr:`name` attribute.
    Otherwise Mutwo will simply initialise the Abjad Pitch from the
    objects :attr:`frequency` attribute.

    If users desire to make more complex conversions (for instance
    due to ``scordatura`` or transpositions of instruments), one can simply
    inherit from this class to define more complex cases.
    """

    def convert(self, pitch_to_convert: parameters.abc.Pitch) -> abjad.Pitch:
        if isinstance(pitch_to_convert, parameters.pitches.WesternPitch):
            return abjad.NamedPitch(pitch_to_convert.name)
        else:
            return abjad.NamedPitch.from_hertz(pitch_to_convert.frequency)


class MutwoPitchToHEJIAbjadPitchConverter(MutwoPitchToAbjadPitchConverter):
    """Convert Mutwo :obj:`~mutwo.parameters.pitches.JustIntonationPitch` objects to Abjad Pitch objects.

    :param reference_pitch: The reference pitch (1/1). Should be a diatonic
        pitch name (see
        :const:`~mutwo.parameters.pitches_constants.ASCENDING_DIATONIC_PITCH_NAMES`)
        in English nomenclature. For any other reference pitch than 'c', Lilyponds
        midi rendering for pitches with the diatonic pitch 'c' will be slightly
        out of tune (because the first value of :arg:`global_scale`
        always have to be 0).
    :type reference_pitch: str, optional
    :param prime_to_heji_accidental_name: Mapping of a prime number
        to a string which indicates the respective prime number in the resulting
        accidental name. See
        :const:`~mutwo.converters.frontends.ekmelily_constants.DEFAULT_PRIME_TO_HEJI_ACCIDENTAL_NAME`
        for the default mapping.
    :type prime_to_heji_accidental_name: dict[int, str], optional
    :param otonality_indicator: String which indicates that the
        respective prime alteration is otonal. See
        :const:`~mutwo.converters.frontends.ekmelily_constants.DEFAULT_OTONALITY_INDICATOR`
        for the default value.
    :type otonality_indicator: str, optional
    :param utonality_indicator: String which indicates that the
        respective prime alteration is utonal. See
        :const:`~mutwo.converters.frontends.ekmelily_constants.DEFAULT_OTONALITY_INDICATOR`
        for the default value.
    :type utonality_indicator: str, optional
    :param exponent_to_exponent_indicator: Function to convert the
        exponent of a prime number to string which indicates the respective
        exponent. See
        :func:`~mutwo.converters.frontends.ekmelily_constants.DEFAULT_EXPONENT_TO_EXPONENT_INDICATOR`
        for the default function.
    :type exponent_to_exponent_indicator: typing.Callable[[int], str], optional
    :param tempered_pitch_indicator: String which indicates that the
        respective accidental is tempered (12 EDO). See
        :const:`~mutwo.converters.frontends.ekmelily_constants.DEFAULT_TEMPERED_PITCH_INDICATOR`
        for the default value.
    :type tempered_pitch_indicator: str, optional

    The resulting Abjad pitches are expected to be used in combination with tuning
    files that are generated by
    :class:`~mutwo.converters.frontends.ekmelily.HEJIEkmelilyTuningFileConverter`
    and with the Lilypond extension
    `Ekmelily <http://www.ekmelic-music.org/en/extra/ekmelily.htm>`_.
    You can find pre-generated tuning files
    `here <https://github.com/levinericzimmermann/ekme-heji.ily>`_.

    **Example:**

    >>> from mutwo.parameters import pitches
    >>> from mutwo.converters.frontends import abjad
    >>> my_ji_pitch = pitches.JustIntonationPitch('5/4')
    >>> converter_on_a = abjad.MutwoPitchToHEJIAbjadPitchConverter(reference_pitch='a')
    >>> converter_on_c = abjad.MutwoPitchToHEJIAbjadPitchConverter(reference_pitch='c')
    >>> converter_on_a.convert(my_ji_pitch)
    NamedPitch("csoaa''")
    >>> converter_on_c.convert(my_ji_pitch)
    NamedPitch("eoaa'")
    """

    class _HEJIAccidental(object):
        """Fake abjad accidental

        Only for internal usage within the :class:`MutwoPitchToHEJIAbjadPitchConverter`.
        """

        def __init__(self, accidental: str):
            self._accidental = accidental

        def __str__(self) -> str:
            return self._accidental

        # necessary attributes, although they
        # won't be used at all
        semitones = 0
        arrow = None

    def __init__(
        self,
        reference_pitch: str = "a",
        prime_to_heji_accidental_name: typing.Optional[dict[int, str]] = None,
        otonality_indicator: str = None,
        utonality_indicator: str = None,
        exponent_to_exponent_indicator: typing.Callable[[int], str] = None,
        tempered_pitch_indicator: str = None,
    ):
        # set default values
        if prime_to_heji_accidental_name is None:
            prime_to_heji_accidental_name = (
                ekmelily_constants.DEFAULT_PRIME_TO_HEJI_ACCIDENTAL_NAME
            )

        if otonality_indicator is None:
            otonality_indicator = ekmelily_constants.DEFAULT_OTONALITY_INDICATOR

        if utonality_indicator is None:
            utonality_indicator = ekmelily_constants.DEFAULT_UTONALITY_INDICATOR

        if exponent_to_exponent_indicator is None:
            exponent_to_exponent_indicator = (
                ekmelily_constants.DEFAULT_EXPONENT_TO_EXPONENT_INDICATOR
            )

        if tempered_pitch_indicator is None:
            tempered_pitch_indicator = (
                ekmelily_constants.DEFAULT_TEMPERED_PITCH_INDICATOR
            )

        self._reference_pitch = reference_pitch
        self._otonality_indicator = otonality_indicator
        self._utonality_indicator = utonality_indicator
        self._exponent_to_exponent_indicator = exponent_to_exponent_indicator
        self._tempered_pitch_indicator = tempered_pitch_indicator
        self._reference_index = (
            parameters.pitches_constants.ASCENDING_DIATONIC_PITCH_NAMES.index(
                reference_pitch
            )
        )
        self._prime_to_heji_accidental_name = prime_to_heji_accidental_name

    def _find_western_octave_for_just_intonation_pitch(
        self,
        pitch_to_convert: parameters.pitches.JustIntonationPitch,
        closest_pythagorean_pitch_name: str,
    ) -> int:
        octave = pitch_to_convert.octave + 4
        closest_pythagorean_pitch_index = (
            parameters.pitches_constants.ASCENDING_DIATONIC_PITCH_NAMES.index(
                closest_pythagorean_pitch_name[0]
            )
        )
        if closest_pythagorean_pitch_index < self._reference_index:
            octave += 1

        pitch_as_western_pitch = parameters.pitches.WesternPitch(
            closest_pythagorean_pitch_name[0], octave
        )
        reference_pitch_as_western_pitch = parameters.pitches.WesternPitch(
            self._reference_pitch, 4
        )
        expected_difference_in_cents = pitch_to_convert.cents
        while (
            expected_difference_in_cents
            - (
                (
                    pitch_as_western_pitch.midi_pitch_number
                    - reference_pitch_as_western_pitch.midi_pitch_number
                )
                * 100
            )
            > 300
        ):
            pitch_as_western_pitch.octave += 1

        while (
            expected_difference_in_cents
            - (
                (
                    pitch_as_western_pitch.midi_pitch_number
                    - reference_pitch_as_western_pitch.midi_pitch_number
                )
                * 100
            )
            < -300
        ):
            pitch_as_western_pitch.octave -= 1

        """
        # for pitches which are written with the same diatonic pitch as
        # the reference_pitch, but which are slightly deeper
        if (
            closest_pythagorean_pitch_index == self._reference_index
            and pitch_to_convert.normalize(mutate=False).cents > 600  # type: ignore
        ):
            octave += 1
        print(octave, closest_pythagorean_pitch_index, self._reference_index, '\n')

        return octave
        """
        return pitch_as_western_pitch.octave

    def _find_heji_accidental_for_just_intonation_pitch(
        self,
        pitch_to_convert: parameters.pitches.JustIntonationPitch,
        abjad_pitch_class: abjad.NamedPitchClass,
    ):
        # find additional commas
        accidental_parts = [str(abjad_pitch_class.accidental)]
        prime_to_exponent = (
            pitch_to_convert.helmholtz_ellis_just_intonation_notation_commas.prime_to_exponent
        )
        for prime in sorted(prime_to_exponent.keys()):
            exponent = prime_to_exponent[prime]
            if exponent != 0:
                tonality = (
                    self._otonality_indicator
                    if exponent > 0
                    else self._utonality_indicator
                )
                heji_accidental_name = self._prime_to_heji_accidental_name[prime]
                exponent_indicator = self._exponent_to_exponent_indicator(
                    abs(exponent) - 1
                )
                accidental_parts.append(
                    f"{tonality}{heji_accidental_name}{exponent_indicator}"
                )

        accidental = self._HEJIAccidental("".join(accidental_parts))
        return accidental

    def _convert_just_intonation_pitch(
        self,
        pitch_to_convert: parameters.pitches.JustIntonationPitch,
    ) -> abjad.Pitch:
        # find pythagorean pitch
        closest_pythagorean_pitch_name = (
            pitch_to_convert.get_closest_pythagorean_pitch_name(self._reference_pitch)
        )
        abjad_pitch_class = abjad.NamedPitchClass(closest_pythagorean_pitch_name)

        accidental = self._find_heji_accidental_for_just_intonation_pitch(
            pitch_to_convert, abjad_pitch_class
        )
        abjad_pitch_class._accidental = accidental

        octave = self._find_western_octave_for_just_intonation_pitch(
            pitch_to_convert, closest_pythagorean_pitch_name
        )

        abjad_pitch = abjad.NamedPitch(octave=octave)
        abjad_pitch._pitch_class = abjad_pitch_class
        return abjad_pitch

    def convert(self, pitch_to_convert: parameters.abc.Pitch) -> abjad.Pitch:
        if isinstance(pitch_to_convert, parameters.pitches.JustIntonationPitch):
            abjad_pitch = self._convert_just_intonation_pitch(pitch_to_convert)
        else:
            abjad_pitch = MutwoPitchToAbjadPitchConverter().convert(pitch_to_convert)

        return abjad_pitch


class MutwoVolumeToAbjadAttachmentDynamicConverter(converters_abc.Converter):
    """Convert Mutwo Volume objects to :class:`~mutwo.converters.frontends.attachments.Dynamic`.

    This default class simply checks if the passed Mutwo object belongs to
    :class:`mutwo.parameters.volumes.WesternVolume`. If it does, Mutwo
    will initialise the :class:`Tempo` object from the :attr:`name` attribute.
    Otherwise Mutwo will first initialise a :class:`WesternVolume` object via
    its py:method:`mutwo.parameters.volumes.WesternVolume.from_amplitude` method.

    Hairpins aren't notated with the aid of :class:`mutwo.parameters.abc.Volume`
    objects, but with :class:`mutwo.parameters.playing_indicators.Hairpin`.
    """

    def convert(
        self, volume_to_convert: parameters.abc.Volume
    ) -> typing.Optional[attachments.Dynamic]:
        if not isinstance(volume_to_convert, parameters.volumes.WesternVolume):
            if volume_to_convert.amplitude > 0:
                volume_to_convert = parameters.volumes.WesternVolume.from_amplitude(
                    volume_to_convert.amplitude
                )
            else:
                return None
        return attachments.Dynamic(dynamic_indicator=volume_to_convert.name)


class TempoEnvelopeToAbjadAttachmentTempoConverter(converters_abc.Converter):
    """Convert tempo envelope to :class:`~mutwo.converters.frontends.attachments.Tempo`.

    Abstract base class for tempo envelope conversion. See
    :class:`ComplexTempoEnvelopeToAbjadAttachmentTempoConverter` for a concrete
    class.
    """

    @abc.abstractmethod
    def convert(
        self, tempo_envelope_to_convert: expenvelope.Envelope
    ) -> tuple[tuple[constants.Real, attachments.Tempo], ...]:
        # return tuple filled with subtuples (leaf_index, attachments.Tempo)
        raise NotImplementedError()


class ComplexTempoEnvelopeToAbjadAttachmentTempoConverter(
    TempoEnvelopeToAbjadAttachmentTempoConverter
):
    """Convert tempo envelope to :class:`~mutwo.converters.frontends.attachments.Tempo`.

    This object tries to intelligently set correct tempo attachments to an
    :class:`abjad.Voice` object, appropriate to Western notation standards.
    Therefore it will not repeat tempo indications if they are merely repetitions
    of previous tempo indications and it will write 'a tempo' when returning to the
    same tempo after ritardandi or accelerandi.
    """

    # ###################################################################### #
    #                     private static methods                             #
    # ###################################################################### #

    @staticmethod
    def _convert_tempo_points(
        tempo_points: tuple[
            typing.Union[constants.Real, parameters.tempos.TempoPoint], ...
        ]
    ) -> tuple[parameters.tempos.TempoPoint, ...]:
        return tuple(
            tempo_point
            if isinstance(tempo_point, parameters.tempos.TempoPoint)
            else parameters.tempos.TempoPoint(float(tempo_point))
            for tempo_point in tempo_points
        )

    @staticmethod
    def _find_dynamic_change_indication(
        tempo_point: parameters.tempos.TempoPoint,
        next_tempo_point: typing.Optional[parameters.tempos.TempoPoint],
    ) -> typing.Optional[str]:
        dynamic_change_indication = None
        if next_tempo_point:
            absolute_tempo_for_current_tempo_point = (
                tempo_point.absolute_tempo_in_beat_per_minute
            )
            absolute_tempo_for_next_tempo_point = (
                next_tempo_point.absolute_tempo_in_beat_per_minute
            )
            if (
                absolute_tempo_for_current_tempo_point
                > absolute_tempo_for_next_tempo_point
            ):
                dynamic_change_indication = "rit."
            elif (
                absolute_tempo_for_current_tempo_point
                < absolute_tempo_for_next_tempo_point
            ):
                dynamic_change_indication = "acc."

        return dynamic_change_indication

    @staticmethod
    def _shall_write_metronome_mark(
        tempo_envelope_to_convert: expenvelope.Envelope,
        nth_tempo_point: int,
        tempo_point: parameters.tempos.TempoPoint,
        tempo_points: tuple[parameters.tempos.TempoPoint, ...],
    ) -> bool:
        write_metronome_mark = True
        for previous_tempo_point, previous_tempo_point_duration in zip(
            reversed(tempo_points[:nth_tempo_point]),
            reversed(tempo_envelope_to_convert.durations[:nth_tempo_point]),
        ):
            # make sure the previous tempo point could have been written
            # down (longer duration than minimal duration)
            if previous_tempo_point_duration > 0:
                # if the previous writeable MetronomeMark has the same
                # beats per minute than the current event, there is no
                # need to write it down again
                if (
                    previous_tempo_point.absolute_tempo_in_beat_per_minute
                    == tempo_point.absolute_tempo_in_beat_per_minute
                ):
                    write_metronome_mark = False
                    break

                # but if it differs, we should definitely write it down
                else:
                    break

        return write_metronome_mark

    @staticmethod
    def _shall_stop_dynamic_change_indication(
        tempo_attachments: tuple[
            tuple[constants.Real, attachments.Tempo], ...
        ]
    ) -> bool:
        stop_dynamic_change_indicaton = False
        for _, previous_tempo_attachment in reversed(tempo_attachments):
            # make sure the previous tempo point could have been written
            # down (longer duration than minimal duration)
            if previous_tempo_attachment.dynamic_change_indication is not None:
                stop_dynamic_change_indicaton = True
            break

        return stop_dynamic_change_indicaton

    @staticmethod
    def _find_metronome_mark_values(
        write_metronome_mark: bool,
        tempo_point: parameters.tempos.TempoPoint,
        stop_dynamic_change_indicaton: bool,
    ) -> tuple[
        typing.Optional[tuple[int, int]],
        typing.Optional[typing.Union[int, tuple[int, int]]],
        typing.Optional[str],
    ]:
        if write_metronome_mark:
            textual_indication: typing.Optional[str] = tempo_point.textual_indication
            reference = fractions.Fraction(tempo_point.reference) * fractions.Fraction(
                1, 4
            )
            reference_duration: typing.Optional[tuple[int, int]] = (
                reference.numerator,
                reference.denominator,
            )
            units_per_minute: typing.Optional[
                typing.Union[int, tuple[int, int]]
            ] = (
                (
                    int(tempo_point.tempo_or_tempo_range_in_beats_per_minute[0]),
                    int(tempo_point.tempo_or_tempo_range_in_beats_per_minute[1]),
                )
                if isinstance(
                    tempo_point.tempo_or_tempo_range_in_beats_per_minute, tuple
                )
                else int(tempo_point.tempo_or_tempo_range_in_beats_per_minute)
            )

        else:
            reference_duration = None
            units_per_minute = None
            # check if you can write 'a tempo'
            if stop_dynamic_change_indicaton:
                textual_indication = "a tempo"
            else:
                textual_indication = None

        return reference_duration, units_per_minute, textual_indication

    @staticmethod
    def _process_tempo_event(
        tempo_envelope_to_convert: expenvelope.Envelope,
        nth_tempo_point: int,
        tempo_point: parameters.tempos.TempoPoint,
        tempo_points: tuple[parameters.tempos.TempoPoint, ...],
        tempo_attachments: tuple[
            tuple[constants.Real, attachments.Tempo], ...
        ],
    ) -> attachments.Tempo:
        try:
            next_tempo_point: typing.Optional[
                parameters.tempos.TempoPoint
            ] = tempo_points[nth_tempo_point + 1]
        except IndexError:
            next_tempo_point = None

        # check for dynamic_change_indication
        dynamic_change_indication = ComplexTempoEnvelopeToAbjadAttachmentTempoConverter._find_dynamic_change_indication(
            tempo_point, next_tempo_point
        )
        write_metronome_mark = ComplexTempoEnvelopeToAbjadAttachmentTempoConverter._shall_write_metronome_mark(
            tempo_envelope_to_convert,
            nth_tempo_point,
            tempo_point,
            tempo_points,
        )

        stop_dynamic_change_indicaton = ComplexTempoEnvelopeToAbjadAttachmentTempoConverter._shall_stop_dynamic_change_indication(
            tempo_attachments
        )

        (
            reference_duration,
            units_per_minute,
            textual_indication,
        ) = ComplexTempoEnvelopeToAbjadAttachmentTempoConverter._find_metronome_mark_values(
            write_metronome_mark, tempo_point, stop_dynamic_change_indicaton
        )

        # for writing 'a tempo'
        if textual_indication == "a tempo":
            write_metronome_mark = True

        converted_tempo_point = attachments.Tempo(
            reference_duration=reference_duration,
            units_per_minute=units_per_minute,
            textual_indication=textual_indication,
            dynamic_change_indication=dynamic_change_indication,
            stop_dynamic_change_indicaton=stop_dynamic_change_indicaton,
            print_metronome_mark=write_metronome_mark,
        )

        return converted_tempo_point

    # ###################################################################### #
    #                           public api                                   #
    # ###################################################################### #

    def convert(
        self, tempo_envelope_to_convert: expenvelope.Envelope
    ) -> tuple[tuple[constants.Real, attachments.Tempo], ...]:
        tempo_points = (
            ComplexTempoEnvelopeToAbjadAttachmentTempoConverter._convert_tempo_points(
                tempo_envelope_to_convert.levels
            )
        )

        tempo_attachments: list[
            tuple[constants.Real, attachments.Tempo]
        ] = []
        for nth_tempo_point, absolute_time, duration, tempo_point in zip(
            range(len(tempo_points)),
            tools.accumulate_from_zero(tempo_envelope_to_convert.durations),
            tempo_envelope_to_convert.durations + (1,),
            tempo_points,
        ):

            if duration > 0:
                tempo_attachment = ComplexTempoEnvelopeToAbjadAttachmentTempoConverter._process_tempo_event(
                    tempo_envelope_to_convert,
                    nth_tempo_point,
                    tempo_point,
                    tempo_points,
                    tuple(tempo_attachments),
                )
                tempo_attachments.append((absolute_time, tempo_attachment))

        return tuple(tempo_attachments)
