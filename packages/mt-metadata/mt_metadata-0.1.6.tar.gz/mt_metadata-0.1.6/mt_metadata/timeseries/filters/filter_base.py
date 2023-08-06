# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:30:36 2020

:copyright: 
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

This is a base class for filters.  We will extend this class for each specific 
type of filter we need to implement.  Typical filters we will want to be able
to support are:
- PoleZero (or 'zpk') responses like those provided by IRIS
- Frequency-Amplitude-Phase (FAP) tables: look up tables from laboratory calibrations via frequency sweep on a spectrum analyser.
- Time Delay Filters: can come about in decimation, or from general timing errors that have been characterized
- Coefficient multipliers, i.e. frequency independent gains
- FIR filters
- IIR filters

Note that many filters can be represented in more than one of these forms.  For example a Coefficient Multiplier can be
seen as an FIR with a single coefficient.  Similarly, an FIR can be represented as a 'zpk' filter with no poles.  An IIR
filter can also be associated with a zpk representation.  However, solving for the 'zpk' representation can be tedious
and approximate and if we have for example, the known FIR coefficients, or FAP lookup table, then there is little
to be gained by changing the representation.

The "stages" that are described in the IRIS StationXML documentation appear to cover all possible linear time invariant
filter types we are likely to encounter.

TESTING:
Several sample station xml files have been archived in the data repository for the purpose of testing the filter
codes. These are described in the readme in mth5_test_data/iris

Passing Tests Means:
-the container has a place for all the (relevant) info in the "Stage"
-The stages (or filters) can be combined,
-desired: Each Stage needs to be able to generate a response function
-The total response function of all the stage can be represented in a way that works with FFTs.

____
Players on the stage:

<ATTR_DICT>
attr_dict: This comes from a json configuration.  This object is not actually of type dictionary.
It does provide us with a bunch of dictionaries .. one per attribute of the Filter() class.
Other attributes are listed here:
['name',
 'type',
 'units_in',
 'units_out',
 'calibration_date',
 'normalization_factor',
 'normalization_frequency',
 'cutoff',
 'operation',
 'n_poles',
 'n_zeros',
 'conversion_factor']

Since some of these attrs have 'required':True, and some have 'required':False, it isn;t
clear to me yet if
a)this is supposed to be an exhaustive list of all possible filter attrs,
b) The list needs to be pared down to just the attrs that every filter will have
c) something else I haven't thought of.
</ATTR_DICT>

<OBSPY_MAPPING>
This is a dictionary that maps attribute names from obspy to the names we use in MTH5.

Note that obspy defines all these filter attributes on __init__:
class ResponseStage(ComparingObject):
#    From the StationXML Definition:
#        This complex type represents channel response and covers SEED
#        blockettes 53 to 56.
 def __init__(self, stage_sequence_number, stage_gain,
                 stage_gain_frequency, input_units, output_units,
                 resource_id=None, resource_id2=None, name=None,
                 input_units_description=None,
                 output_units_description=None, description=None,
                 decimation_input_sample_rate=None, decimation_factor=None,
                 decimation_offset=None, decimation_delay=None,
                 decimation_correction=None):

</OBSPY_MAPPING>

<RELATIONSHIP TO OPBSPY>
This is not yet 100% well defined.  We do require the ability to populate our Filter() objects from obspy.
It is desireable to map an arbitrary filter back into an obspy stage, and this could possibly be done
directly or by casting it to xml and
</RELATIONSHIP TO OPBSPY>
<TODO>
add a helper function to identify when the decimation information in the obspy class is degenerate,
such as set to None, or decimation_factor == 1.0.

Review code in obspy/core/inventory/response.py
This seems to contain the functionality we want ... makes me wonder if we should just wrap this with calls?

TAI: Currently we are casting time delay filters from stages that have degenerate decimation, but decimation_delay
non-zero.  However, we should ask this question: Are there filters that we may expect to encounter that have
both a time_delay and a non-identity response inasmuchas amplitude an phase? If so we want to address whether it is
appropriate the factor these filters into a delay part and an "ampl/phase" part... is this legal?

StageGain Is A hard requirement of both IRIS and OBSPY.  Let's play nice and add a gain to our base class.

COMBINE?
Filters Combine Method ... do we keep time delay and others as separate entitites?
If so, what do we do with decimation filters that have an inate time delay?
# def combine(self, other):
#     # TODO: Add checks here that when you are stitching two filters together the
#     # output_units of the before filter match the input units of the after
#     Parameters
#     ----------
#     other
#
#     Returns a filter that has the combined complex response of the product of
#     self and other.  The assumption is the the output of self matches to the imput of other.
#     -------
#
#     print("units consistency check:")
#     print("self output {}".format(self.output_units))
#     print("other input {}".format(other.input_units))
#
#     cr1 = lambda f: self.complex_response(f)
#     cr2 = lambda f: other.complex_response(f)
#     cr3 = lambda f: cr1(f) * cr2(f)
#     self.lambda_function = cr3
COMBINE?
</TODO>
"""
# =============================================================================
# Imports
# =============================================================================
import copy
import obspy
import numpy as np

from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from mt_metadata.base.helpers import filter_descriptions
from mt_metadata.utils.units import get_unit_object, Unit
from mt_metadata.timeseries.filters.plotting_helpers import plot_response
from mt_metadata.timeseries.filters.standards import SCHEMA_FN_PATHS
from mt_metadata.utils.mttime import MTime


# =============================================================================
attr_dict = get_schema("filter_base", SCHEMA_FN_PATHS)
# =============================================================================

# Form is OBSPY_MAPPING['obspy_label'] = 'mth5_label'
OBSPY_MAPPING = {}
OBSPY_MAPPING["input_units"] = "units_in"
OBSPY_MAPPING["name"] = "name"
OBSPY_MAPPING["output_units"] = "units_out"
OBSPY_MAPPING["stage_gain"] = "gain"
OBSPY_MAPPING["description"] = "comments"


class FilterBase(Base):
    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        """

        Parameters
        ----------
        kwargs
        name: The label for this filter, can act as a key for response info
        type: One of {'pole_zero', 'frequency_table', 'coefficient', 'fir', 'iir', 'time_delay'}
        units_in: expected units of data coming from the previous stage ...
        ? is this defined by the data itself? Or is this an Idealized Value?
        normalization_frequency: ???
        normalization_factor ???
        cutoff

        """

        self.name = None
        self.type = None
        self._units_in_obj = Unit()
        self._units_out_obj = Unit()

        self._calibration_dt = MTime()
        self.comments = None
        self.obspy_mapping = copy.deepcopy(OBSPY_MAPPING)
        self.gain = 1.0

        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def obspy_mapping(self):
        return self._obspy_mapping

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is not None:
            self._name = str(value).lower().replace("/", " per ")
        else:
            self._name = None

    @obspy_mapping.setter
    def obspy_mapping(self, obspy_dict):
        """
        set the obspy mapping: this is a dictionary relating attribute labels from obspy stage objects to
        mt_metadata filter objects.
        """
        if not isinstance(obspy_dict, dict):
            msg = f"Input must be a dictionary not {type(obspy_dict)}"
            self.logger.error(msg)
            raise TypeError(msg)

        self._obspy_mapping = obspy_dict

    @property
    def calibration_date(self):
        return self._calibration_dt.date

    @calibration_date.setter
    def calibration_date(self, value):
        self._calibration_dt.from_str(value)

    @property
    def total_gain(self):
        return self.gain

    @property
    def units_in(self):
        return self._units_in_obj.abbreviation

    @units_in.setter
    def units_in(self, value):
        self._units_in_obj = get_unit_object(value)

    @property
    def units_out(self):
        return self._units_out_obj.abbreviation

    @units_out.setter
    def units_out(self, value):
        self._units_out_obj = get_unit_object(value)

    def get_filter_description(self):
        """

        :param filter_type: DESCRIPTION
        :type filter_type: TYPE
        :return: DESCRIPTION
        :rtype: TYPE

        """

        if self.comments is None:
            return filter_descriptions[self.type]

        return self.comments

    @classmethod
    def from_obspy_stage(cls, stage, mapping=None):
        """
        purpose of this method is to un-bloat the obspy stage dictionary which typically
        contains a lot of extraneous information.
        If you want to propagate all that info : you can make a mapping which is basically
        dict(zip(stage.__dict__.keys(), stage.__dict__.keys()),
        or we could maybe support something cleaner...

        Parameters
        ----------
        stage:
        mapping

        Returns
        -------

        """
        if not isinstance(stage, obspy.core.inventory.response.ResponseStage):
            print("Expected a Stage and got a {}".format(type(stage)))
            raise Exception

        if mapping is None:
            mapping = cls().obspy_mapping
        kwargs = {}
        for obspy_label, mth5_label in mapping.items():
            try:
                kwargs[mth5_label] = stage.__dict__[obspy_label]
            except KeyError:
                print(f"Key {obspy_label} not found in stage object")
                raise Exception

        return cls(**kwargs)

    def complex_response(self, frqs):
        print("Filter Base class does not have a complex response defined")
        return None

    def pass_band(self, frequencies, window_len=5, tol=0.5, **kwargs):
        """

        Caveat: This should work for most Fluxgate and feedback coil magnetometers, and basically most filters
        having a "low" number of poles and zeros.  This method is not 100% robust to filters with a notch in them.

        Try to estimate pass band of the filter from the flattest spots in
        the amplitude.

        The flattest spot is determined by calculating a sliding window
        with length `window_len` and estimating normalized std.

        ..note:: This only works for simple filters with
        on flat pass band.

        :param window_len: length of sliding window in points
        :type window_len: integer

        :param tol: the ratio of the mean/std should be around 1
        tol is the range around 1 to find the flat part of the curve.
        :type tol: float

        :return: pass band frequencies
        :rtype: np.ndarray

        """

        f = frequencies
        cr = self.complex_response(f, **kwargs)
        amp = np.abs(cr)
        # precision is apparently an important variable here
        if np.round(amp, 6).all() == np.round(amp.mean(), 6):
            return np.array([f.min(), f.max()])

        f_true = np.zeros_like(frequencies)
        for ii in range(0, f.size - window_len, 1):
            cr_window = np.array(amp[ii : ii + window_len])  # / self.amplitudes.max()
            test = abs(1 - np.log10(cr_window.min()) / np.log10(cr_window.max()))

            if test <= tol:
                f_true[(f >= f[ii]) & (f <= f[ii + window_len])] = 1

        pb_zones = np.reshape(np.diff(np.r_[0, f_true, 0]).nonzero()[0], (-1, 2))

        if pb_zones.shape[0] > 1:
            self.logger.debug(
                f"Found {pb_zones.shape[0]} possible pass bands, using the longest. "
                "Use the estimated pass band with caution."
            )
        # pick the longest
        try:
            longest = np.argmax(np.diff(pb_zones, axis=1))
            if pb_zones[longest, 1] >= f.size:
                pb_zones[longest, 1] = f.size - 1
        except ValueError:
            self.logger.warning(
                "No pass band could be found within the given frequency range. Returning None"
            )
            return None

        return np.array([f[pb_zones[longest, 0]], f[pb_zones[longest, 1]]])

    def generate_frequency_axis(self, sampling_rate, n_observations):
        dt = 1.0 / sampling_rate
        frequency_axis = np.fft.fftfreq(n_observations, d=dt)
        frequency_axis = np.fft.fftshift(frequency_axis)
        return frequency_axis

    def plot_response(
        self,
        frequencies,
        x_units="period",
        unwrap=True,
        pb_tol=1e-1,
        interpolation_method="slinear",
    ):
        if frequencies is None:
            frequencies = self.generate_frequency_axis(10.0, 1000)
            x_units = "frequency"

        kwargs = {
            "title": self.name,
            "unwrap": unwrap,
            "x_units": x_units,
            "label": self.name,
        }

        complex_response = self.complex_response(
            frequencies, **{"interpolation_method": interpolation_method}
        )
        if hasattr(self, "poles"):
            kwargs["poles"] = self.poles
            kwargs["zeros"] = self.zeros

        if hasattr(self, "pass_band"):
            kwargs["pass_band"] = self.pass_band(
                frequencies,
                tol=pb_tol,
                **{"interpolation_method": interpolation_method},
            )

        plot_response(frequencies, complex_response, **kwargs)

    @property
    def decimation_active(self):
        if hasattr(self, "decimation_factor"):
            if self.decimation_factor != 1.0:
                return True
        return False

    def apply(self, ts):
        data_spectum = ts.fft()
        complex_response = self.complex_response(ts.frequencies)
        calibrated_spectrum = data_spectum / complex_response
        calibrated_data = np.fft.ifft(calibrated_spectrum)
        output = ts._deepcopy()
        output.data = calibrated_data
        return output
