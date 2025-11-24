#!/usr/bin/env bash

setup() {
    #
    # Prepare local variables
    #

    local this_file="$( [ ! -z "${ZSH_VERSION}" ] && echo "${(%):-%x}" || echo "${BASH_SOURCE[0]}" )"
    local this_dir="$( cd "$( dirname "${this_file}" )" && pwd )"
    local orig="${PWD}"
    local setup_name="${1:-shi_default}"


    #
    # Export base directory
    #

    export SHI_BASE="${this_dir}"
    echo "Single Higgs Combinations base: ${SHI_BASE}"


    #
    # Override Combine and CMSSW versions BEFORE sourcing combine_workflow setup
    #

    export CWF_COMBINE_VERSION="${CWF_COMBINE_VERSION:-v10.0.0}"
    export CWF_CMSSW_VERSION="${CWF_CMSSW_VERSION:-CMSSW_11_3_4}"
    export CWF_SCRAM_ARCH="${CWF_SCRAM_ARCH:-slc7_amd64_gcc900}"

    echo "Using Combine ${CWF_COMBINE_VERSION} with ${CWF_CMSSW_VERSION}"


    #
    # Pre-populate setup file with version overrides (if first time)
    #

    local setup_file="${SHI_BASE}/.setups/${setup_name}.sh"
    if [ ! -f "${setup_file}" ]; then
        mkdir -p "${SHI_BASE}/.setups"
        echo "# SHI setup file for: ${setup_name}" > "${setup_file}"
        echo "# Auto-generated with custom Combine/CMSSW versions" >> "${setup_file}"
        echo "" >> "${setup_file}"
        echo "export CWF_CMSSW_VERSION=\"${CWF_CMSSW_VERSION}\"" >> "${setup_file}"
        echo "export CWF_COMBINE_VERSION=\"${CWF_COMBINE_VERSION}\"" >> "${setup_file}"
        echo "" >> "${setup_file}"
        echo "# Additional settings will be added by combine_workflow/setup.sh during first run" >> "${setup_file}"

        echo ""
        echo "Created setup file with custom Combine/CMSSW versions: ${setup_file}"
        echo "The combine_workflow setup will now prompt for user-specific settings..."
        echo ""
    fi


    #
    # Source the combine_workflow setup
    #

    if [ ! -f "${SHI_BASE}/combine_workflow/setup.sh" ]; then
        >&2 echo "ERROR: combine_workflow/setup.sh not found!"
        >&2 echo "       Please ensure the combine_workflow submodule is initialized:"
        >&2 echo "       git submodule update --init --recursive"
        return 1
    fi

    # Mark that we're using custom setup
    export SHI_CUSTOM_SETUP="1"

    # Source combine_workflow setup with the same setup name
    source "${SHI_BASE}/combine_workflow/setup.sh" "${setup_name}" || return "$?"


    #
    # Override CWF paths to use absolute paths instead of relative
    #

    export CWF_DATA="${SHI_BASE}/data"
    export CWF_STORE="${CWF_DATA}/store"
    export CWF_STORE_JOBS="${CWF_STORE}"
    export CWF_STORE_BUNDLES="${CWF_STORE}"
    export CWF_SOFTWARE="${CWF_DATA}/software"


    #
    # Add SHI module to Python path
    #

    local pyv="$( python3 -c "import sys; print('{0.major}.{0.minor}'.format(sys.version_info))" )"
    export PYTHONPATH="${SHI_BASE}:${PYTHONPATH}"

    # Update PATH for custom scripts if needed
    export PATH="${SHI_BASE}/bin:${PATH}"


    #
    # Store setup name
    #

    export SHI_SETUP_NAME="${setup_name}"


    #
    # Law setup for SHI tasks
    #

    # Override LAW_CONFIG_FILE to use SHI law.cfg (which inherits from combine_workflow)
    export LAW_CONFIG_FILE="${SHI_BASE}/law.cfg"

    if which law &> /dev/null; then
        # Re-index to include SHI tasks
        law index -q
    fi

    cd "${orig}"
}

action() {
    if setup "$@"; then
        echo -e "\x1b[0;49;35mSingle Higgs Combination tools successfully setup\x1b[0m"
        echo "  - Combine version: ${CWF_COMBINE_VERSION}"
        echo "  - CMSSW version: ${CWF_CMSSW_VERSION}"
        echo "  - Setup name: ${SHI_SETUP_NAME}"
        echo "  - SHI tasks available in 'shi.tasks'"
        return "0"
    else
        local code="$?"
        echo -e "\x1b[0;49;31msetup failed with code ${code}\x1b[0m"
        return "${code}"
    fi
}

action "$@"
